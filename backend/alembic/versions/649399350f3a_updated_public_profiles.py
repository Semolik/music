"""updated public profiles

Revision ID: 649399350f3a
Revises: 64c22a1903a9
Create Date: 2022-10-30 13:01:19.763677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649399350f3a'
down_revision = '64c22a1903a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('public_profiles', sa.Column('picture_id', sa.Integer(), nullable=True))
    op.add_column('public_profiles', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'public_profiles', 'files', ['picture_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'public_profiles', 'users', ['user_id'], ['id'])
    op.drop_constraint('public_profiles_links_picture_id_fkey', 'public_profiles_links', type_='foreignkey')
    op.drop_column('public_profiles_links', 'picture_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('public_profiles_links', sa.Column('picture_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('public_profiles_links_picture_id_fkey', 'public_profiles_links', 'files', ['picture_id'], ['id'], ondelete='SET NULL')
    op.drop_constraint(None, 'public_profiles', type_='foreignkey')
    op.drop_constraint(None, 'public_profiles', type_='foreignkey')
    op.drop_column('public_profiles', 'user_id')
    op.drop_column('public_profiles', 'picture_id')
    # ### end Alembic commands ###
