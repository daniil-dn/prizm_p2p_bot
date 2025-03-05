"""update orders

Revision ID: a501d2fc8b55
Revises: d4065dac1b08
Create Date: 2025-03-04 18:36:28.115421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a501d2fc8b55'
down_revision = 'd4065dac1b08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_from_to_currency_count', table_name='order_request')
    op.create_index('ix_from_to_currency_count', 'order_request', ['from_currency', 'to_currency', 'min_limit', 'max_limit'], unique=False)
    op.add_column('transaction', sa.Column('user_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_transaction_user_id'), 'transaction', ['user_id'], unique=False)
    op.create_foreign_key(None, 'transaction', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_index(op.f('ix_transaction_user_id'), table_name='transaction')
    op.drop_column('transaction', 'user_id')
    op.drop_index('ix_from_to_currency_count', table_name='order_request')
    op.create_index('ix_from_to_currency_count', 'order_request', ['from_currency', 'to_currency', 'min_limit_rub', 'max_limit_rub'], unique=False)
    # ### end Alembic commands ###
