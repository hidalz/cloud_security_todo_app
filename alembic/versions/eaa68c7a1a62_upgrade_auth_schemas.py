"""Upgrade auth schemas

Revision ID: eaa68c7a1a62
Revises: f8d4b4764884
Create Date: 2023-08-15 13:11:43.780380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaa68c7a1a62'
down_revision: Union[str, None] = 'f8d4b4764884'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###