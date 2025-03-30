from unittest.mock import AsyncMock

import pytest

from repositories.modules.wallet.dto import CreateWalletDTO
from services import WalletService, _TronService
from services.tron.exceptions import WalletNotFoundServiceException


@pytest.mark.asyncio
async def test_add_request_with_valid_address(
    wallet_service: tuple[WalletService, _TronService],
):
    address = "VALID_TRON_ADDRESS"
    service, tron = wallet_service

    # FIXME: Перенести в фикстуру вместе с моком трона
    tron.get_account_info = AsyncMock(
        return_value=CreateWalletDTO(
            address=address,
            bandwidth=100.0,
            energy=10.0,
            trx_balance=200.0,
        )
    )

    await service.get_wallet_info_and_create_request(address)

    result = await service.repository.get_list()

    assert len(result) == 1, "Result shouldn't be empty"


@pytest.mark.asyncio
async def test_dont_add_request_with_invalid_address(
    wallet_service: tuple[WalletService, _TronService],
):
    address = "INVALID_TRON_ADDRESS"
    service, tron = wallet_service

    tron.get_account_info = AsyncMock(side_effect=WalletNotFoundServiceException())

    with pytest.raises(
        WalletNotFoundServiceException,
    ):
        await service.get_wallet_info_and_create_request(address)

    result = await service.repository.get_list()

    assert len(result) == 0, "Result should be empty"
