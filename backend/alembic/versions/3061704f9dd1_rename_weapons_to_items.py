"""rename weapons to items

Revision ID: 3061704f9dd1
Revises: 51833416da5e
Create Date: 2025-12-12 03:35:57.912457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3061704f9dd1'
down_revision: Union[str, None] = '51833416da5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
