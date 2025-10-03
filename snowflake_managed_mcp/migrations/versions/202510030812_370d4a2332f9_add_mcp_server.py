"""add_mcp_server

Revision ID: 370d4a2332f9
Revises: 1fcb7ff99c41
Create Date: 2025-10-03 08:12:25.138316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '370d4a2332f9'
down_revision: Union[str, Sequence[str], None] = '1fcb7ff99c41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    create or replace mcp server MCP_SERVER from specification
        $$
        tools:
          - name: "Get_Feature_Requests"
            identifier: "USER_FEATURE_REQUESTS"
            type: "CORTEX_SEARCH_SERVICE_QUERY"
            description: "A tool that performs keyword and vector search over user feature requests for our application."
            title: "Feature Requests"
        $$;
    """)


def downgrade() -> None:
    op.execute("""
    DROP MCP SERVER MCP_SERVER;
    """)
