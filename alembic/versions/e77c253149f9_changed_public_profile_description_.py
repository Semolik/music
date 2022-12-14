"""changed public profile description length

Revision ID: e77c253149f9
Revises: 1e32c82abce2
Create Date: 2022-11-26 21:42:18.328942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e77c253149f9'
down_revision = '1e32c82abce2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('public_profiles', 'description',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('public_profiles', 'description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)
    # ### end Alembic commands ###
