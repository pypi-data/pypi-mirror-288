import asyncio
import os
from typing import Any, AsyncGenerator, Coroutine, Dict, Generator, List, Optional

import openai
from fastapi import HTTPException
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel, Field

from llmstudio.engine.providers.provider import ChatRequest, Provider, provider


class AzureParameters(BaseModel):
    temperature: Optional[float] = Field(default=1, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=2048, ge=1)
    top_p: Optional[float] = Field(default=1, ge=0, le=1)
    frequency_penalty: Optional[float] = Field(default=0, ge=0, le=1)
    presence_penalty: Optional[float] = Field(default=0, ge=0, le=1)


class AzureRequest(ChatRequest):
    api_endpoint: Optional[str] = None
    api_version: Optional[str] = None
    base_url: Optional[str] = None
    parameters: Optional[AzureParameters] = AzureParameters()
    functions: Optional[List[Dict[str, Any]]] = None
    chat_input: Any
    response_format: Optional[Dict[str, str]] = None


@provider
class AzureProvider(Provider):
    def __init__(self, config):
        super().__init__(config)
        self.API_KEY = os.getenv("AZURE_API_KEY")
        self.API_ENDPOINT = os.getenv("AZURE_API_ENDPOINT")
        self.API_VERSION = os.getenv("AZURE_API_VERSION")
        self.BASE_URL = os.getenv("AZURE_BASE_URL")

    def validate_request(self, request: AzureRequest):
        return AzureRequest(**request)

    async def generate_client(
        self, request: AzureRequest
    ) -> Coroutine[Any, Any, Generator]:
        """Generate an AzureOpenAI client"""
        try:
            if request.base_url or self.BASE_URL:
                client = OpenAI(
                    api_key=request.api_key or self.API_KEY,
                    base_url=request.base_url or self.BASE_URL,
                )
                return await asyncio.to_thread(
                    client.chat.completions.create,
                    model=request.model,
                    messages=(
                        [{"role": "user", "content": request.chat_input}]
                        if isinstance(request.chat_input, str)
                        else request.chat_input
                    ),
                    stream=True,
                )
            else:
                client = AzureOpenAI(
                    api_key=request.api_key or self.API_KEY,
                    azure_endpoint=request.api_endpoint or self.API_ENDPOINT,
                    api_version=request.api_version or self.API_VERSION,
                )
                return await asyncio.to_thread(
                    client.chat.completions.create,
                    model=request.model,
                    messages=(
                        [{"role": "user", "content": request.chat_input}]
                        if isinstance(request.chat_input, str)
                        else request.chat_input
                    ),
                    functions=request.functions,
                    function_call="auto" if request.functions else None,
                    stream=True,
                    response_format=request.response_format,
                    **request.parameters.model_dump(),
                )

        except openai._exceptions.APIError as e:
            raise HTTPException(status_code=e.status_code, detail=e.response.json())

    async def parse_response(
        self, response: AsyncGenerator, **kwargs
    ) -> AsyncGenerator[str, None]:
        for chunk in response:
            yield chunk.model_dump()
