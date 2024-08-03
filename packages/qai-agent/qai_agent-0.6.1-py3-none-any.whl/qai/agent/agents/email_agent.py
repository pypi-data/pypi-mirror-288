import os
import time
from functools import partial
from logging import getLogger
from typing import Callable, List, Optional, Self, Type, Union
from uuid import UUID, uuid4

import requests
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import AgentChatResponse
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.chat_engine.types import AgentChatResponse
from llama_index.core.llms import ChatMessage
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.tools import BaseTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.core.tools.types import BaseTool
from pydantic import BaseModel, Field
from pymongo import MongoClient

from qai.agent import ROOT_DIR, cfg
from pi_blink import blink
from qai.agent.utils.distribute import adistribute
from qai.agent.utils.schema_utils import get_name

log = getLogger(__name__)
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR)))

example_template = """"""
job_title_template = """, who holds the job title {job_title}"""
industry_template = """Industry of {company_name} is {industry}"""
default_template = """
Generate a professional and engaging email from a person named {from_name}{from_job_title_template} from {from_company}, 
addressed to another person named {to_name}{to_job_title_template} from {to_company}.

Rules:

1. Include a subject line and a body.
2. The body should consist of one or two paragraph only, not including tables or making comparisons.
3. The language should be straightforward and devoid of embellishments.
4. Incorporate relevant details about the technologies used by both companies, as well as the industries they operate in, only if it enhances the email’s relevance or context.
5. Format the email to reflect standard business communication practices, including appropriate greetings, paragraph breaks, and closings.

Additional Context:
{from_industry_template}
{to_industry_template}

{example_template}
"""


class EmailModel(BaseModel):
    """
    Email Model for the email tool.
    body is the body of the email with correct punctuation and newlines and spacing.
    """

    subject: str = Field(description="The subject of the email.")
    body_list: list[str] = Field(
        description="The body of the email as a list of str. There can be empty lines in the list."
    )

    email: Optional[str] = Field(description="The email address of the person.", default=None)
    name: Optional[str] = Field(description="The name of the person.", default=None)
    phone: Optional[str] = Field(description="The phone number of the person.", default=None)
    id: Optional[UUID] = Field(description="Id of the email for tracking", default_factory=uuid4)

    @property
    def body(self) -> str:
        return "\n".join(self.body_list)

    def dict(self):
        return {"subject": self.subject, "body": self.body, "email": self.email}


class OnEmailCompleteEvent(BaseModel):
    sequence_id: str
    email: EmailModel
    cancel: bool = False


class OnAllEmailsCompletedEvent(BaseModel):
    sequence_id: str
    successes: int
    errors: int
    cancel: bool = False


class EmailToolSpec(BaseToolSpec):
    """Tool for emails."""

    template: str = None
    spec_functions = ["draft_email"]
    from_person: dict
    from_company: dict

    def __init__(
        self,
        from_person: dict,
        from_company: dict,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.from_person = from_person
        self.from_company = from_company

    def create_prompt(
        self,
        from_person: dict,
        from_company: dict,
        to_person: dict,
        to_company: dict,
    ) -> str:
        """
        Create a prompt for the email.
        Args:
            from_person (dict): The person sending the email.
            from_company (dict): The company sending the email.
            to_person (dict): The person receiving the email.
            to_company (dict): The company receiving the email.

        """
        from_name = get_name(from_person)
        to_name = get_name(to_person)

        from_company_name = self.get_cname(from_company)
        to_company_name = self.get_cname(to_company)

        from_job_title = from_person.get("job_title")
        to_job_title = to_person.get("job_title")
        from_job_title_template = (
            "" if not from_job_title else job_title_template.format(job_title=from_job_title)
        )
        to_job_title_template = (
            "" if not to_job_title else job_title_template.format(job_title=to_job_title)
        )
        from_company_industry = from_company.get("industry")
        to_company_industry = to_company.get("industry")

        from_industry_template = ""
        if from_company_industry:
            from_industry_template = industry_template.format(
                company_name=from_company_name, industry=from_company_industry
            )
        to_industry_template = ""
        if to_company_industry:
            to_industry_template = industry_template.format(
                company_name=to_company_name, industry=to_company_industry
            )

        s = default_template.format(
            from_name=from_name,
            from_company=from_company_name,
            to_name=to_name,
            to_company=to_company_name,
            from_job_title_template=from_job_title_template,
            to_job_title_template=to_job_title_template,
            from_industry_template=from_industry_template,
            to_industry_template=to_industry_template,
            example_template=example_template,
        )
        return s

    def get_cname(self, company: dict) -> str:
        """
        Get the company name from the company dict.
        """
        cname = company.get("company_name")
        if not cname:
            cname = company.get("name")
        if not cname:
            raise ValueError(f"Company must have a name. values={company}")
        return cname

    def draft_email(
        self,
        to_person: dict,
        to_company: dict,
        prompt: str | None = None,
        callback: Callable | None = None,
    ) -> EmailModel:
        """
        Draft an email for a person.
        """
        prompt = prompt or self.create_prompt(
            self.from_person,
            self.from_company,
            to_person,
            to_company,
        )

        # email = EmailModel(subject=data["subject"], body=data["body"])
        ## TODO - Email body is not being generated with correct formatting when using json output.
        ## using a default fixes it but the call needs to be manually parsed.
        program = LLMTextCompletionProgram.from_defaults(
            output_cls=EmailModel, prompt_template_str=prompt, verbose=True
        )
        email: EmailModel = program()
        email.email = to_person.get("email")
        email.name = to_person.get("name")
        email.phone = to_person.get("phone")
        if callback:
            callback(email)
        return email

    @staticmethod
    def _create_email(
        from_person: dict,
        from_company: dict,
        to_person: dict,
        to_company: dict,
        template: Optional[str] = None,
        email_callback: Optional[Callable] = None,
        email_tool_spec_cls: Type["EmailToolSpec"] = None,
    ) -> EmailModel:
        log.debug(f"Creating email from {from_person} to {to_person}")
        log.debug(f"  From Company: {from_company} To Company: {to_company}")
        if email_tool_spec_cls is None:
            email_tool_spec_cls = EmailToolSpec
        company_email = to_person.get("email")
        if company_email:
            company_email = company_email.split("@")[1]
        to_company = {
            "name": company_email,
        }
        if not to_company:
            raise ValueError(f"Company not found for person {to_person}")
        draft_tool = email_tool_spec_cls(from_person=from_person, from_company=from_company)
        email = draft_tool.draft_email(
            to_person=to_person,
            to_company=to_company,
            callback=email_callback,
        )

        return email

    @staticmethod
    def _create_emails(
        kwargs_list: list[dict],
        on_all_complete: Optional[Callable] = None,
        asynchronous: bool = True,
        email_tool_spec_cls: Self = Self,
    ) -> None | List[EmailModel]:
        if asynchronous:
            adistribute(
                email_tool_spec_cls._create_email,
                kwargs_list=kwargs_list,
                on_all_complete=on_all_complete,
                nprocs=4,
            )
        else:
            emails = []
            successes = 0
            errors = 0
            for kwargs in kwargs_list:
                kwargs["email_tool_spec_cls"] = email_tool_spec_cls
                try:
                    emails.append(email_tool_spec_cls._create_email(**kwargs))
                    successes += 1
                except Exception as e:
                    log.exception(f"Error creating email: {e}")
                    errors += 1
            if on_all_complete:
                on_all_complete(successes, errors)
            return emails


class EmailAgent(OpenAIAgent):

    def __init__(self, email_tool_spec_cls: EmailToolSpec = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email_tool_spec_cls = email_tool_spec_cls or EmailToolSpec

    def chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Optional[Union[str, dict]] = None,
    ) -> AgentChatResponse:
        return super().chat(message, chat_history, tool_choice)

    @staticmethod
    def _on_all_emails_complete(sequence_id: str, successes: int, errors: int) -> None:
        event = OnAllEmailsCompletedEvent(
            sequence_id=sequence_id, successes=successes, errors=errors
        )
        blink.send(event)

    def create_emails(
        self,
        sequence_id: str,
        from_person: dict,
        from_company: dict,
        to_people: dict,
        to_companies: Optional[dict] = None,
        use_async_on: Optional[int] = None,
    ) -> List[EmailModel]:
        """
        Create the emails for the campaign.
        Args:
            None
        Returns:
            A list of EmailModel objects.
        """
        log.debug("Sending emails")
        if to_companies is None:
            to_companies = {}
        email_params = []
        async_emails_params = []

        ### Resolve the company for each person

        for i, person_id in enumerate(to_people.keys()):
            to_person = to_people[person_id]
            if "company_id" in to_person:
                to_company = to_companies.get(to_person["company_id"])
            try:
                if not to_company:
                    to_company = {"name": to_person.get("email").split("@")[1]}
            except:
                to_company = {
                    "name": "Unknown",
                }
            params = {
                "from_person": from_person,
                "from_company": from_company,
                "to_person": to_person,
                "to_company": to_company,
            }
            log.debug(
                f"Creating email for {to_person} to {to_company} from {from_person} {from_company}"
            )
            f = partial(self.on_email_complete, sequence_id)
            params["email_callback"] = f

            if use_async_on is None or i < use_async_on:
                email_params.append(params)
            else:
                async_emails_params.append(params)
        if async_emails_params:
            f = partial(self._on_all_emails_complete, sequence_id)
            ## TODO resolve potential issue of async completing before
            # all sync emails are generated. and sending message before
            self.email_tool_spec_cls._create_emails(
                kwargs_list=async_emails_params,
                on_all_complete=f,
                asynchronous=True,
                email_tool_spec_cls=self.email_tool_spec_cls,
            )
        emails = []
        if email_params:
            f = None
            if not async_emails_params:
                f = partial(self._on_all_emails_complete, sequence_id)
            emails = self.email_tool_spec_cls._create_emails(
                kwargs_list=email_params,
                on_all_complete=f,
                asynchronous=False,
                email_tool_spec_cls=self.email_tool_spec_cls,
            )
        return emails

    @staticmethod
    @blink.listener(OnEmailCompleteEvent)
    def on_email_complete(event: OnEmailCompleteEvent) -> None:
        sequence_id = event.sequence_id
        email = event.email
        log.debug(f"Email completed: {sequence_id} {email}")
        mongo = cfg.mongo
        client = MongoClient(mongo.uri)
        db = client[mongo.db]

        collection = db[mongo.collection]
        js = {
            "sequence_id": sequence_id,
            "prospect_email": email.email,
            "prospect_name": email.name,
            "prospect_phone": email.phone,
            "message_subject": email.subject,
            "message_body": email.body,
            "is_message_generation_complete": True,
        }
        log.debug(f"Inserting into collection: {mongo.uri} {db} {collection.name} ")
        result = collection.insert_one(js)
        log.debug(f"Insert Result: {result}")

    @staticmethod
    @blink.listener(OnAllEmailsCompletedEvent)
    def on_all_emails_complete(event: OnAllEmailsCompletedEvent) -> None:
        sequence_id = event.sequence_id
        successes = event.successes
        errors = event.errors
        # log.debug(f"All Email completed: {successes} success, {errors} errors.")
        print(f"!!!!!!!!!!!!!!!!!!! All Email completed: {successes} success, {errors} errors.")
        # url = cfg.email.on_complete_emails_url
        # log.debug(f"Sending call to {url}  sequence_id={sequence_id}")
        # delay = cfg.email.get("delay_complete_request", 0)
        # if delay:
        #     time.sleep(delay)
        # r = requests.post(url, json={"sequence_id": sequence_id})
        # log.debug(r.json())

    @classmethod
    def create(
        cls,
        from_person: dict = None,
        from_company: dict = None,
        tools: List[BaseTool] = None,
        email_tool_spec_cls: EmailToolSpec = EmailToolSpec,
    ) -> Self:
        if not tools:
            if not from_person:
                raise ValueError("from_person must be provided.")
            spec = email_tool_spec_cls(from_person, from_company)
            tools = spec.to_tool_list()
        agent = cls.from_tools(tools)
        agent.email_tool_spec_cls = email_tool_spec_cls
        return agent
