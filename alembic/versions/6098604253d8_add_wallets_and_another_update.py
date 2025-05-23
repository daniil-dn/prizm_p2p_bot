"""add wallets and another update

Revision ID: 6098604253d8
Revises: f70effe195f1
Create Date: 2025-02-25 16:06:09.739959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6098604253d8'
down_revision = 'f70effe195f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_request', sa.BigInteger(), nullable=False))
    op.add_column('order', sa.Column('from_value', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False))
    op.add_column('order', sa.Column('to_value', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False))
    op.create_foreign_key(None, 'order', 'order_request', ['order_request'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'to_value')
    op.drop_column('order', 'from_value')
    op.drop_column('order', 'order_request')
    # ### end Alembic commands ###
