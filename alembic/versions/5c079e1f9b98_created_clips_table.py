"""created clips table

Revision ID: 5c079e1f9b98
Revises: 3f5f980f977a
Create Date: 2022-11-27 01:11:42.794881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c079e1f9b98'
down_revision = '3f5f980f977a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('video_id', sa.String(length=12), nullable=False),
    sa.Column('picture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['picture_id'], ['files.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clips_id'), 'clips', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clips_id'), table_name='clips')
    op.drop_table('clips')
    # ### end Alembic commands ###
