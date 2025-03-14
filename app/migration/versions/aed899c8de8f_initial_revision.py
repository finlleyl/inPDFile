"""Initial revision

Revision ID: aed899c8de8f
Revises: b1125d198391
Create Date: 2025-02-24 22:03:40.412761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aed899c8de8f'
down_revision: Union[str, None] = 'b1125d198391'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_confirmations', sa.Column('is_used', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_confirmations', 'is_used')
    # ### end Alembic commands ###
