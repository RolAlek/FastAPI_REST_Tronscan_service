from dataclasses import dataclass

from domain.models.wallets import Wallet
from repositories.base import BaseSQLAlchemyRepository
from repositories.modules.wallet.dto import CreateWalletDTO


@dataclass
class WalletRepository(BaseSQLAlchemyRepository[Wallet, CreateWalletDTO]):
    model = Wallet
