"""Initial database baseline

Revision ID: 332a2ebed3eb
Revises:
Create Date: 2026-08-26 12:00:06.760695

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "332a2ebed3eb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Add the column temporarily allowing NULL
    op.add_column(
        "orders",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    # 2. Give existing orders a timestamp
    op.execute(
        "UPDATE orders SET created_at = NOW() "
        "WHERE created_at IS NULL"
    )

    # 3. Make the column required
    op.alter_column(
        "orders",
        "created_at",
        nullable=False
    )

    # 4. Automatically timestamp future orders
    op.alter_column(
        "orders",
        "created_at",
        server_default=sa.text("now()")
    )


def downgrade() -> None:

    op.drop_column(
        "orders",
        "created_at"
    )