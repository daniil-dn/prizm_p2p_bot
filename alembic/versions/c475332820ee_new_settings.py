"""new settings

Revision ID: c475332820ee
Revises: 520a6f45311a
Create Date: 2025-03-27 14:28:11.617014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c475332820ee'
down_revision = '520a6f45311a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('settings', sa.Column('minimum_referal_withdrawal_amount', sa.Numeric(precision=18, scale=2, asdecimal=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'minimum_referal_withdrawal_amount')
    # ### end Alembic commands ###
