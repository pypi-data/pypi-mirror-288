from typing import Optional
import httpx
import uvicorn
from .extension_agent_factory import ExtensionAgentFactory
from .extension_metadata import ExtensionMetadata
from .base_extension import BaseExtension
from langchain_openai_api_bridge.fastapi.langchain_openai_api_bridge_fastapi import (
    LangchainOpenaiApiBridgeFastAPI,
)
from fastapi import FastAPI


class ExtensionHost:
    def __init__(
        self,
        extension: BaseExtension,
        port: Optional[int] = 7680,
        inference_url: Optional[str] = None,
        inference_http_client: httpx.Client | None = None,
    ) -> None:
        self.extension = extension
        self.port = port

        self.app = FastAPI()
        self.bridge = LangchainOpenaiApiBridgeFastAPI(
            app=self.app,
            agent_factory_provider=ExtensionAgentFactory(
                extension=self.extension,
                inference_url=inference_url,
                http_client=inference_http_client,
            ),
        )

        self._setup_routes()
        self.setup()

    def _setup_routes(self):
        @self.app.get("/metadata")
        def get_metadata():
            return ExtensionMetadata(
                name=self.extension.name(),
                description=self.extension.description(),
            )

        self.bridge.bind_openai_chat_completion()

    def setup(self):
        if hasattr(self.extension, "setup"):
            self.extension.setup()

    def start_server(self):
        uvicorn.run(self.app, host="localhost", port=self.port)
