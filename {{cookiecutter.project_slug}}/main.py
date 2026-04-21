from app.core.config import config
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.origins import make_middleware, init_routers
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run code at startup and shutdown using lifespan context."""
    # Startup
    logger.info("Starting FastAPI app...")

    yield  # This is where the app runs

    # Shutdown
    logger.info("Shutting down FastAPI app...")

def create_app() -> FastAPI:

    app_ = FastAPI(
        middleware=make_middleware(),
        title="Template FastAPI",
        description="Template FastAPI",
        version="V1.0",
    )

    init_routers(app_=app_)
    logger.info("FastAPI application created successfully.")
    return app_


app = create_app()

if __name__ == "__main__":
    import uvicorn

    def get_host_port(url: str) -> tuple[str, int]:
        if url.startswith("http://"):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]
        host, port = url.split(":")
        return host, int(port)

    host, port = get_host_port(config.BACKEND_URL)
    if config.DEBUG:
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        uvicorn.run(app, host=host, port=port)
