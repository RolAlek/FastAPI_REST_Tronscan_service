import itertools
from collections.abc import Iterable
from functools import lru_cache

from aioinject import Container, Scoped, Singleton
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.config import (APISettings, DatabaseSettings,
                                     TronAPISettings)
from application.di.modules.wallet import PROVIDERS as WALLET_PROVIDERS
from repositories.dependencies import get_session

MODULES = [WALLET_PROVIDERS]
SETTINGS = [APISettings, DatabaseSettings, TronAPISettings]


def _register_settings(
    container: Container,
    *,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        container.register(Singleton(settings_cls))


@lru_cache
def init_container() -> Container:
    container = Container()

    container.register(Scoped(get_session, type_=AsyncSession))

    for provider in itertools.chain.from_iterable(MODULES):
        container.register(provider)

    _register_settings(container, settings_classes=SETTINGS)

    return container
