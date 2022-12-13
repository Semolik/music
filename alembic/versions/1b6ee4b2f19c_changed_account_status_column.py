"""changed account status column

Revision ID: 1b6ee4b2f19c
Revises: 08934a327f78
Create Date: 2022-12-07 23:58:17.035426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b6ee4b2f19c'
down_revision = '08934a327f78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('type', sa.String(), nullable=True))
    op.drop_column('users', 'is_radio_station')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_musician')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_musician', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_radio_station', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'type')
    # ### end Alembic commands ###
