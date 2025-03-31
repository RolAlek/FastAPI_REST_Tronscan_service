from datetime import datetime
from uuid import UUID

from pydantic import Field

from application.api.handlers.schemas import BaseSchema


class WalletRequestSchema(BaseSchema):
    address: str = Field(..., min_length=3)


class WalletRequestResponseSchema(BaseSchema):
    oid: UUID
    address: str
    bandwidth: float
    energy: float
    trx_balance: float
    created_at: datetime
