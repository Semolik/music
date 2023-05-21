"""changed history_item ids to uuid

Revision ID: a7bc7d70234b
Revises: c85fb88dc441
Create Date: 2023-04-30 22:16:17.340593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a7bc7d70234b'
down_revision = 'c85fb88dc441'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('listen_album_history', 'id',
               existing_type=sa.INTEGER(),
               type_=postgresql.UUID(as_uuid=True),
               existing_nullable=False)
    op.alter_column('listen_musician_history', 'id',
               existing_type=sa.INTEGER(),
               type_=postgresql.UUID(as_uuid=True),
               existing_nullable=False)
    op.alter_column('listen_playlist_history', 'id',
               existing_type=sa.INTEGER(),
               type_=postgresql.UUID(as_uuid=True),
               existing_nullable=False)
    op.alter_column('listen_track_history', 'id',
               existing_type=sa.INTEGER(),
               type_=postgresql.UUID(as_uuid=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('listen_track_history', 'id',
               existing_type=postgresql.UUID(as_uuid=True),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('listen_playlist_history', 'id',
               existing_type=postgresql.UUID(as_uuid=True),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('listen_musician_history', 'id',
               existing_type=postgresql.UUID(as_uuid=True),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('listen_album_history', 'id',
               existing_type=postgresql.UUID(as_uuid=True),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###