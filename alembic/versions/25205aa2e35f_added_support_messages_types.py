"""added support messages types

Revision ID: 25205aa2e35f
Revises: 
Create Date: 2023-06-18 00:28:59.666314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25205aa2e35f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('support_messages', sa.Column('type', sa.Enum('PASSWORD_RECOVERY', 'SUPPORT', name='supportmessagetype'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('support_messages', 'type')
    # ### end Alembic commands ###