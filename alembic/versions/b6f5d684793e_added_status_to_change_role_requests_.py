"""added status to change_role_requests table

Revision ID: b6f5d684793e
Revises: ae7074b66d2c
Create Date: 2022-10-15 11:18:53.730863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6f5d684793e'
down_revision = 'ae7074b66d2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('change_role_requests', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('change_role_requests', 'status')
    # ### end Alembic commands ###
