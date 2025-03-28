from typing import Annotated

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Form, HTTPException, status
from result import Err

from application.api.handlers.wallets.shcemas import WalletResponseSchema
from services.tron.exceptions import WalletNotFoundServiceException
from services.wallet.service import WalletService

router = APIRouter()


@router.post("/", response_model=WalletResponseSchema)
@inject
async def create_wallet(
    address: Annotated[str, Form()],
    service: Injected[WalletService],
):
    result = await service.get_wallet_info(address)

    if isinstance(result, Err):
        match result.err_value:
            case WalletNotFoundServiceException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Wallet from address `{address}` not found.",
                )

    return result
