import signal
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from loguru import logger


def signal_handler(signum: Any, _: Any) -> None:
    logger.info(f"Received signal ({signal.Signals(signum).name})", "shutting down server...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Server starting up...")
    yield
    logger.info("Server shutdown successfully")


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=PlainTextResponse)
async def handler() -> str:
    return "cloudflare-workers-containers-python-template"


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        timeout_graceful_shutdown=5,
    )
