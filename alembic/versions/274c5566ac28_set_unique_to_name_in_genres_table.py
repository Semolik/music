"""set unique to name in genres table

Revision ID: 274c5566ac28
Revises: f84619e22f11
Create Date: 2022-11-08 01:03:44.787561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '274c5566ac28'
down_revision = 'f84619e22f11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'genres', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'genres', type_='unique')
    # ### end Alembic commands ###
