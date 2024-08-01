"""added_chat_history_fix

Revision ID: 1e7f3dc15e9c
Revises: b8fe483b5a71
Create Date: 2024-05-06 15:24:26.996166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1e7f3dc15e9c'
down_revision: Union[str, None] = 'b8fe483b5a71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat_history', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_history', sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
