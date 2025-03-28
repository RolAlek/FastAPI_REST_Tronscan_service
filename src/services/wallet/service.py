from dataclasses import dataclass

from result import Err

from repositories.modules.wallet.repository import WalletRepository
from services.tron.service import _TronService


@dataclass
class WalletService:
    service: _TronService
    repository: WalletRepository

    async def get_wallet_info(self, address: str):
        response = await self.service.get_account_info(address)

        if isinstance(response, Err):
            return response

        instance = await self.repository.add(response)

        return instance
