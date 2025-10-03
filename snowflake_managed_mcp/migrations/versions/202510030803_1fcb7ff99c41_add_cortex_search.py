"""add_cortex_search

Revision ID: 1fcb7ff99c41
Revises: e2390ebd39f5
Create Date: 2025-10-03 08:03:17.939917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fcb7ff99c41'
down_revision: Union[str, Sequence[str], None] = 'e2390ebd39f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE CORTEX SEARCH SERVICE FEATURE_REQUEST_SEARCH
        ON MESSAGE
        ATTRIBUTES USER_ID, CREATED_AT
        WAREHOUSE = COMPUTE_WH
        TARGET_LAG = '1 hour'
        AS (
            SELECT USER_ID, MESSAGE, CREATED_AT
            FROM USER_FEATURE_REQUESTS
        );
    """)


def downgrade() -> None:
    op.execute("""
        DROP CORTEX SEARCH SERVICE FEATURE_REQUEST_SEARCH
    """)
