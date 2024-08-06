from typing import Optional
import httpx
from langchain_openai_api_bridge.core.base_agent_factory import BaseAgentFactory
from .base_extension import BaseExtension
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_openai_api_bridge.core.create_agent_dto import CreateAgentDto


class ExtensionAgentFactory(BaseAgentFactory):

    def __init__(
        self,
        extension: BaseExtension,
        inference_url: Optional[str],
        http_client: httpx.Client | None = None,
    ) -> None:
        self.extension = extension
        self.inference_url = inference_url
        self.http_client = http_client

    def create_agent(self, dto: CreateAgentDto) -> Runnable:
        return self.extension.create_runnable(
            llm=ChatOpenAI(
                base_url=self.inference_url,
                http_client=self.http_client,
                temperature=dto.temperature or 0.7,
                model=dto.model,
                max_tokens=dto.max_tokens,
                api_key=dto.api_key,
            )
        )
