# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""The EmbeddingsLLM class."""

from promptflow.tracing import trace
from typing_extensions import Unpack

from graphrag.llm.base import BaseLLM
from graphrag.llm.types import EmbeddingInput, EmbeddingOutput, LLMInput

from .openai_configuration import OpenAIConfiguration
from .types import OpenAIClientTypes


class OpenAIEmbeddingsLLM(BaseLLM[EmbeddingInput, EmbeddingOutput]):
    """A text-embedding generator LLM."""

    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        self.client = client
        self.configuration = configuration

    @trace
    async def _execute_llm(
        self, input: EmbeddingInput, **kwargs: Unpack[LLMInput]
    ) -> EmbeddingOutput | None:
        args = {
            "model": self.configuration.model,
            **(kwargs.get("model_parameters") or {}),
        }
        embedding = await self.client.embeddings.create(
            input=input,
            **args,
        )
        return [d.embedding for d in embedding.data]
