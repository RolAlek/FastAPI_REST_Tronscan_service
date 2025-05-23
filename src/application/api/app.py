from contextlib import aclosing, asynccontextmanager
from typing import AsyncIterator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.api.exceptions import BaseHTTPError
from application.api.handlers import main_router
from application.di.container import init_container


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa: ARG001 - required by lifespan protocol
) -> AsyncIterator[None]:
    async with aclosing(init_container()):
        yield


async def http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: "BaseHTTPError",
) -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder(exc.error_schema.model_dump(by_alias=True)),
        status_code=exc.status_code,
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="FasAPI Tron Scanner",
        docs_url="/api/docs",
        lifespan=_lifespan,
    )
    app.exception_handlers[BaseHTTPError] = http_exception_handler
    app.include_router(main_router)
    app.add_middleware(AioInjectMiddleware, container=init_container())

    return app
