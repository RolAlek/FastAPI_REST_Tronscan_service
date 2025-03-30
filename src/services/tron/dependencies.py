from contextlib import asynccontextmanager
from typing import AsyncIterable

from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from application.core.config import settings


@asynccontextmanager
async def get_tron_client() -> AsyncIterable[AsyncTron]:
    async with AsyncTron(AsyncHTTPProvider(api_key=settings.tron.api_key)) as client:
        yield client
