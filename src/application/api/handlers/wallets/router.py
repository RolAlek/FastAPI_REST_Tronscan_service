from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.default import Params
from result import Err

from application.api.handlers.wallets import exceptions as api_exceptions
from application.api.handlers.wallets.responses import \
    get_wallet_info_responses
from application.api.handlers.wallets.schemas import (
    WalletRequestResponseSchema, WalletRequestSchema)
from services.tron import exceptions as app_exceptions
from services.wallet.service import WalletService

router = APIRouter()


@router.post(
    "/",
    response_model=WalletRequestResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=get_wallet_info_responses,
)
@inject
async def request_wallet(
    data: WalletRequestSchema,
    service: Injected[WalletService],
):
    """
    This endpoint gets wallet info and saves request for the given address.
    """
    result = await service.get_wallet_info_and_create_request(data.address)

    if isinstance(result, Err):
        match result.err_value:
            case app_exceptions.WalletNotFoundServiceException():
                raise api_exceptions.NotFoundAddressHTTPException(data.address)
            case app_exceptions.WalletAddressFormatInvalidException():
                raise api_exceptions.InvalidFormatAddressHTTPException(data.address)

    return result


@router.get("/", response_model=Page[WalletRequestResponseSchema])
@inject
async def get_requests(
    service: Injected[WalletService],
    params: Params = Depends(),
):
    """
    This endpoint returns all requests to get wallet info with pagination.
    """
    return await service.get_request_info(params)
