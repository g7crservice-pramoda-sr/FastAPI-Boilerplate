from typing import List
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.root.connector import root_route
from app.core.config import config


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=config.ALLOWED_HOSTS,
            allow_credentials=True,
            allow_methods=config.ALLOWED_METHODS,
            allow_headers=config.ALLOWED_HEADERS,
        ),
    ]
    return middleware


def init_routers(app_: FastAPI) -> None:
    app_.include_router(root_route)
