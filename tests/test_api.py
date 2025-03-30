from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from result import Err

from repositories.modules.wallet.dto import CreateWalletDTO
from services.tron.exceptions import (
    WalletAddressFormatInvalidException,
    WalletNotFoundServiceException,
)
from services.tron.service import _TronService


@pytest.mark.asyncio
@patch.object(_TronService, "get_account_info", new_callable=AsyncMock)
async def test_create_request_api(
    mocked_method: AsyncMock, client: TestClient, app: FastAPI
):
    address = "VALID_ADDRESS"
    mocked_method.return_value = CreateWalletDTO(
        address=address,
        bandwidth=100.0,
        energy=10.0,
        trx_balance=200.0,
    )
    url = app.url_path_for("request_wallet")
    response = client.post(url=url, json={"address": address})

    assert response.status_code == 201
    assert response.json()["address"] == address


@patch.object(_TronService, "get_account_info", new_callable=AsyncMock)
def test_create_request_api_with_not_found_address(
    mock_method: AsyncMock, client: TestClient, app: FastAPI
):
    address = "INVALID_ADDRESS"
    mock_method.return_value = Err(WalletNotFoundServiceException())

    url = app.url_path_for("request_wallet")
    response = client.post(url=url, json={"address": address})

    assert response.status_code == 404


@patch.object(_TronService, "get_account_info", new_callable=AsyncMock)
def test_create_request_api_with_bad_address(
    mock_method: AsyncMock, client: TestClient, app: FastAPI
):
    address = "INVALID_ADDRESS"
    mock_method.return_value = Err(WalletAddressFormatInvalidException())

    url = app.url_path_for("request_wallet")
    response = client.post(url=url, json={"address": address})

    assert response.status_code == 400
