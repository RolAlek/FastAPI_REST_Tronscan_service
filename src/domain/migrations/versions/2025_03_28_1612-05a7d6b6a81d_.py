"""empty message

Revision ID: 05a7d6b6a81d
Revises:
Create Date: 2025-03-28 16:12:14.641803

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "05a7d6b6a81d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "wallets",
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("bandwidth", sa.Float(), nullable=False),
        sa.Column("energy", sa.Float(), nullable=False),
        sa.Column("trx_balance", sa.Float(), nullable=False),
        sa.Column("oid", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("oid"),
    )
    op.create_index(
        op.f("ix_wallets_address"),
        "wallets",
        ["address"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f("ix_wallets_address"), table_name="wallets")
    op.drop_table("wallets")
