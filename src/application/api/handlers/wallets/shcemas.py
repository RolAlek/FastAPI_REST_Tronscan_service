from datetime import datetime
from uuid import UUID

from application.api.handlers.schemas import BaseSchema


class WalletResponseSchema(BaseSchema):
    oid: UUID
    address: str
    bandwidth: float
    energy: float
    trx_balance: float
    created_at: datetime
