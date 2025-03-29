from dataclasses import dataclass

from fastapi_pagination.default import Params
from result import Err

from repositories.modules.wallet.repository import WalletRepository
from services.tron.service import _TronService


@dataclass
class WalletService:
    service: _TronService
    repository: WalletRepository

    async def get_wallet_info_and_create_request(self, address: str):
        response = await self.service.get_account_info(address)

        if isinstance(response, Err):
            return response

        return await self.repository.add(response)

    async def get_request_info(self, params: Params):
        return await self.repository.get_requests(params)
