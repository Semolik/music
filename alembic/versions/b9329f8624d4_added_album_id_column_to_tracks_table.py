"""added album_id column to tracks table

Revision ID: b9329f8624d4
Revises: 03ab21e35cc9
Create Date: 2022-11-04 21:09:24.599102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9329f8624d4'
down_revision = '03ab21e35cc9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tracks', sa.Column('album_id', sa.Integer(), nullable=False))
    op.add_column('tracks', sa.Column('file_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tracks', 'albums', ['album_id'], ['id'])
    op.create_foreign_key(None, 'tracks', 'files', ['file_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.drop_column('tracks', 'file_id')
    op.drop_column('tracks', 'album_id')
    # ### end Alembic commands ###
