"""added index=True to Track.name

Revision ID: 651cb14b6bc9
Revises: 118c78146e2c
Create Date: 2023-02-16 20:24:11.295880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '651cb14b6bc9'
down_revision = '118c78146e2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_tracks_name'), 'tracks', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tracks_name'), table_name='tracks')
    # ### end Alembic commands ###
