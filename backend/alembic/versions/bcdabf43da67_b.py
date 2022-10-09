"""b

Revision ID: bcdabf43da67
Revises: aaccb5f8477c
Create Date: 2022-10-07 20:51:11.865073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcdabf43da67'
down_revision = 'aaccb5f8477c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('picture_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'users', ['picture_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'picture_id')
    # ### end Alembic commands ###