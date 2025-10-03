"""add_network_policies_for_pat_access

Revision ID: 60f8b5746c54
Revises: 370d4a2332f9
Create Date: 2025-10-03 08:30:46.453991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60f8b5746c54'
down_revision: Union[str, Sequence[str], None] = '370d4a2332f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE NETWORK POLICY ALLOW_ALL_IPS
    ALLOWED_IP_LIST = ('0.0.0.0/0')
    BLOCKED_IP_LIST = ()
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP NETWORK POLICY ALLOW_ALL_IPS
    """)
