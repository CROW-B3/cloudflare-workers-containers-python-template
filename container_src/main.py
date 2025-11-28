import os
import signal
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn


# Graceful shutdown handler
shutdown_event = False


def signal_handler(signum, frame):
    global shutdown_event
    print(f"Received signal ({signal.Signals(signum).name}), shutting down server...")
    shutdown_event = True
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Server starting up...")
    yield
    # Shutdown
    print("Server shutdown successfully")


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=PlainTextResponse)
@app.get("/container", response_class=PlainTextResponse)
async def handler():
    """
    Main handler that returns the MESSAGE environment variable
    and the Cloudflare Durable Object ID.
    """
    message = os.getenv("MESSAGE", "")
    instance_id = os.getenv("CLOUDFLARE_DURABLE_OBJECT_ID", "")
    return f'Hi, I\'m a container and this is my message: "{message}", my instance ID is: {instance_id}'


@app.get("/error")
async def error_handler():
    """
    Error handler that raises an exception (equivalent to Go panic).
    """
    raise HTTPException(status_code=500, detail="This is a panic")


if __name__ == "__main__":
    print("Server listening on :8080")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        timeout_graceful_shutdown=5,
    )
