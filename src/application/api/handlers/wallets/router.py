from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.default import Params
from result import Err

from application.api.handlers.wallets.shcemas import (
    WalletRequestResponseSchema,
    WalletRequestSchema,
)
from services.tron.exceptions import (
    WalletAddressFormatInvalidException,
    WalletNotFoundServiceException,
)
from services.wallet.service import WalletService

router = APIRouter()


@router.post(
    "/",
    response_model=WalletRequestResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def request_wallet(
    data: WalletRequestSchema,
    service: Injected[WalletService],
):
    result = await service.get_wallet_info_and_create_request(data.address)

    if isinstance(result, Err):
        match result.err_value:
            case WalletNotFoundServiceException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Wallet from address `{data.address}` not found.",
                )
            case WalletAddressFormatInvalidException():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Address `{data.address}` is invalid.",
                )

    return result


@router.get("/", response_model=Page[WalletRequestResponseSchema])
@inject
async def get_requests(
    service: Injected[WalletService],
    params: Params = Depends(),
):
    return await service.get_request_info(params)
