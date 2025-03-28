from contextlib import aclosing
from typing import AsyncIterator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI

from application.api.handlers import main_router
from application.di.container import init_container


async def _lifespan(
        app: FastAPI,    # noqa: ARG001 - required by lifespan protocol 
) -> AsyncIterator[None]:
    async with aclosing(init_container()):
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="FasAPI Tron Scanner",
        docs_url="/api/docs",
        lifespan=_lifespan,
    )
    app.include_router(main_router)
    app.add_middleware(AioInjectMiddleware, container=init_container())

    return app
