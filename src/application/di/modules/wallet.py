from aioinject import Scoped
from tronpy import AsyncTron

from application.di.values import Providers
from repositories.modules.wallet.repository import WalletRepository
from services.tron.dependencies import get_tron_client
from services.tron.service import _TronService
from services.wallet.service import WalletService

PROVIDERS: Providers = [
    Scoped(get_tron_client, type_=AsyncTron),
    Scoped(WalletRepository),
    Scoped(_TronService),
    Scoped(WalletService),
]
