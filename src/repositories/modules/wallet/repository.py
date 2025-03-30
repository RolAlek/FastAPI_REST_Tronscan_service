from dataclasses import dataclass

from fastapi_pagination.default import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from domain.models.wallets import Wallet
from repositories.base import BaseSQLAlchemyRepository
from repositories.modules.wallet.dto import CreateWalletDTO


@dataclass
class _WalletRepository(BaseSQLAlchemyRepository[Wallet, CreateWalletDTO]):
    model = Wallet

    async def get_requests(self, params: Params):
        stmt = select(self.model).order_by(self.model.created_at.desc())

        return await paginate(
            self.session,
            query=stmt,
            params=params,
            subquery_count=True,
        )
