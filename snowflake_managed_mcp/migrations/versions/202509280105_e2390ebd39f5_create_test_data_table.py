"""Create Table with test data

Revision ID: e2390ebd39f5
Revises:
Create Date: 2025-09-28 01:05:32.785183

"""
from typing import Sequence, Union

from alembic import op
import pandas as pd


# revision identifiers, used by Alembic.
revision: str = 'e2390ebd39f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE USER_FEATURE_REQUESTS (
            USER_ID TEXT NOT NULL,
            CREATED_AT TIMESTAMP NOT NULL,
            MESSAGE TEXT NOT NULL
        );
    """)
    pd.read_csv("test_data/feature_request_table.csv").to_sql("user_feature_requests",
                                                              con=op.get_bind(),
                                                              if_exists="append",
                                                              index=False, chunksize=1000, method="multi")


def downgrade() -> None:
    op.execute("""
        DROP TABLE USER_FEATURE_REQUESTS
    """)