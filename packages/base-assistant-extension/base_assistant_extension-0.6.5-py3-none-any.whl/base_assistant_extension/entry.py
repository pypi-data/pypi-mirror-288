import argparse
from base_assistant_extension import (
    ExtensionHost,
)

from .base_extension import BaseExtension


def entry(
    extension: BaseExtension,
    default_port: int = 7680,
    default_inference_url: str = None,
) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=default_port, help="Port number")
    parser.add_argument(
        "--inference_url", type=str, default=default_inference_url, help="Inference url"
    )
    args = parser.parse_args()

    host = ExtensionHost(
        extension=extension,
        inference_url=args.inference_url,
        port=args.port,
    )
    host.start_server()
