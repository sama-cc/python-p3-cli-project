"""changed attribute users to owbers and games to games_owned

Revision ID: 64b7c8d08c3f
Revises: 61817f5c75da
Create Date: 2023-08-22 02:10:38.514318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64b7c8d08c3f'
down_revision: Union[str, None] = '61817f5c75da'
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
