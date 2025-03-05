"""order commission_percent

Revision ID: 20519a7d7d91
Revises: 5b6908c7daeb
Create Date: 2025-02-25 16:29:07.577842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20519a7d7d91'
down_revision = '5b6908c7daeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('commission_percent', sa.Numeric(precision=18, scale=2, asdecimal=False), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'commission_percent')
    # ### end Alembic commands ###
