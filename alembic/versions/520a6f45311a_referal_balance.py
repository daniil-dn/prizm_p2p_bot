"""referal_balance

Revision ID: 520a6f45311a
Revises: 9a31b92fa1ef
Create Date: 2025-03-25 15:55:40.633107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '520a6f45311a'
down_revision = '9a31b92fa1ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'referral_balance',
               existing_type=sa.NUMERIC(precision=18, scale=4),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'referral_balance',
               existing_type=sa.NUMERIC(precision=18, scale=4),
               nullable=True)
    # ### end Alembic commands ###
