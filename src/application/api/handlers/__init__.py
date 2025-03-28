from fastapi import APIRouter

from .wallets.router import router as wallets_router

main_router = APIRouter(prefix="/api")

main_router.include_router(wallets_router, prefix="/wallets", tags=["Wallets"])
