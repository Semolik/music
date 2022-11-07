"""added grenres column

Revision ID: e234df00b05f
Revises: c459d4dc4810
Create Date: 2022-11-08 00:30:28.362857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e234df00b05f'
down_revision = 'c459d4dc4810'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('picture_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['picture_id'], ['files.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genres_id'), 'genres', ['id'], unique=False)
    op.add_column('albums', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'albums', 'genres', ['genre_id'], ['id'])
    op.add_column('tracks', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tracks', 'genres', ['genre_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.drop_column('tracks', 'genre_id')
    op.drop_constraint(None, 'albums', type_='foreignkey')
    op.drop_column('albums', 'genre_id')
    op.drop_index(op.f('ix_genres_id'), table_name='genres')
    op.drop_table('genres')
    # ### end Alembic commands ###
