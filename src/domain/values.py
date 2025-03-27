from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import UUID as SaUUID
from sqlalchemy import func
from sqlalchemy.orm import mapped_column

uuid_pk = Annotated[
    UUID, mapped_column(SaUUID(as_uuid=True), primary_key=True, default=uuid4)
]
_created_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    ),
]

_updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.now(),
    ),
]
