""" remove album_genre_associations model

Revision ID: acf2c5ca39ca
Revises: 0d6f094eb175
Create Date: 2022-12-08 21:15:30.170734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acf2c5ca39ca'
down_revision = '0d6f094eb175'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums_genres_table',
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('album_id', 'genre_id')
    )
    op.drop_table('albums_genres')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums_genres',
    sa.Column('album_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], name='albums_genres_album_id_fkey'),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name='albums_genres_genre_id_fkey'),
    sa.PrimaryKeyConstraint('album_id', 'genre_id', name='albums_genres_pkey')
    )
    op.drop_table('albums_genres_table')
    # ### end Alembic commands ###