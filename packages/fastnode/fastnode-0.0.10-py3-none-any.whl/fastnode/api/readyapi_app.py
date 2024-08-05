from typing import Any, Dict

from readyapi import ReadyAPI, status
from readyapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from fastnode import Fastnode
from fastnode.api.readyapi_utils import patch_readyapi


def launch_api(fastnode_path: str, port: int = 8501, host: str = "0.0.0.0") -> None:
    import uvicorn

    from fastnode import Fastnode
    from fastnode.api import create_api

    app = create_api(Fastnode(fastnode_path))
    uvicorn.run(app, host=host, port=port, log_level="info")


def create_api(fastnode: Fastnode) -> ReadyAPI:

    title = fastnode.name
    if "fastnode" not in fastnode.name.lower():
        title += " - Fastnode"

    # TODO what about version?
    app = ReadyAPI(title=title, description=fastnode.description)

    patch_readyapi(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post(
        "/call",
        operation_id="call",
        response_model=fastnode.output_type,
        # response_model_exclude_unset=True,
        summary="Execute the fastnode.",
        status_code=status.HTTP_200_OK,
    )
    def call(input: fastnode.input_type) -> Any:  # type: ignore
        """Executes this fastnode."""
        return fastnode(input)

    @app.get(
        "/info",
        operation_id="info",
        response_model=Dict,
        # response_model_exclude_unset=True,
        summary="Get info metadata.",
        status_code=status.HTTP_200_OK,
    )
    def info() -> Any:  # type: ignore
        """Returns informational metadata about this Fastnode."""
        return {}

    # Redirect to docs
    @app.get("/", include_in_schema=False)
    def root() -> Any:
        return RedirectResponse("./docs")

    return app
