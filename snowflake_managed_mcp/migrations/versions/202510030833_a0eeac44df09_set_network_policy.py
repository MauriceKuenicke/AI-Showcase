"""set_network_policy

Revision ID: a0eeac44df09
Revises: 60f8b5746c54
Create Date: 2025-10-03 08:33:27.713935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0eeac44df09'
down_revision: Union[str, Sequence[str], None] = '60f8b5746c54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER ACCOUNT SET NETWORK_POLICY = 'ALLOW_ALL_IPS'
    """)


def downgrade() -> None:
    op.execute("""
    ALTER ACCOUNT UNSET NETWORK_POLICY
    """)
