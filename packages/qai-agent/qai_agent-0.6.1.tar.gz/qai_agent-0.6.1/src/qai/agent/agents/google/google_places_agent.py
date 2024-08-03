from typing import Optional, TypeVar

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.llms import ChatMessage
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.core.memory.types import BaseMemory
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.openai import OpenAI
from pi_conf import load_config
from qai.ai import MessageRole
from qai.ai.frameworks.openai.llm import OpenAILLM

from qai.agent.tools.google.google_places import (
    Circle,
    GooglePlaces,
    PlaceType,
    SearchNearbyField,
    TextSearchField,
)

T = TypeVar("T", AgentRunner)


class GooglePlacesToolSpec(BaseToolSpec):
    spec_functions = ["search_nearby"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search_nearby(
        self,
        included_types: list[str | PlaceType],
        circle: Circle,
        fields: SearchNearbyField | list[PlaceType | str],
        maxResultCount: int = 10,
    ) -> dict:
        """
        Search for companies within a circular radius of a center point.
        Args:
            included_types: List of place types to include in search.
            circle: Circle object with a center using latitude and longitude and radius.
            fields: List of fields to return.
            maxResultCount: Maximum number of results to return.
        Returns:
            dict: Dictionary of search results.
        """
        places = GooglePlaces()
        places.search_nearby(
            included_types=included_types,
            circle=circle,
            fields=fields,
            maxResultCount=maxResultCount,
        )

    def text_search(
        self,
        text_query: str,
        fields: TextSearchField | list[PlaceType | str],
        maxResultCount: int = 10,
        **kwargs,
    ) -> dict:
        """
        Search for companies using a text query.
        Args:
            text_query: Text query to search for.
            fields: List of fields to return.
            maxResultCount: Maximum number of results to return.
        Returns:
            dict: Dictionary of search results.
        """
        places = GooglePlaces()
        places.text_search(
            text_query=text_query,
            fields=fields,
            maxResultCount=maxResultCount,
            **kwargs,
        )


class GooglePlacesAgent(OpenAIAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
