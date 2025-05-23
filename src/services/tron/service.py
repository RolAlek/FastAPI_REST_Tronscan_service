from dataclasses import dataclass

from result import Err
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound, BadAddress

from repositories.modules.wallet.dto import CreateWalletDTO
from services.tron.exceptions import (WalletAddressFormatInvalidException,
                                      WalletNotFoundServiceException)


@dataclass
class _TronService:
    client: AsyncTron

    async def get_account_info(self, address: str):
        try:
            trx_balance = await self.client.get_account_balance(address)
            resources = await self.client.get_account_resource(address)
        except AddressNotFound:
            return Err(WalletNotFoundServiceException())
        except BadAddress:
            return Err(WalletAddressFormatInvalidException())

        return CreateWalletDTO(
            address=address,
            bandwidth=resources.get("freeNetLimit"),
            energy=resources.get("TotalEnergyLimit"),
            trx_balance=trx_balance,
        )
