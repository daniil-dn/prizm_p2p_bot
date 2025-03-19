"""add message table

Revision ID: 2b590ca74696
Revises: 8b7e02705f72
Create Date: 2025-03-19 18:37:05.907033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b590ca74696'
down_revision = '8b7e02705f72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_between',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.BigInteger(), nullable=True),
    sa.Column('from_user_id', sa.BigInteger(), nullable=True),
    sa.Column('to_user_id', sa.BigInteger(), nullable=True),
    sa.Column('text', sa.String(length=4096), nullable=True),
    sa.Column('photo', sa.String(length=60), nullable=True),
    sa.Column('document', sa.String(length=60), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_between_created_at'), 'message_between', ['created_at'], unique=False)
    op.create_index(op.f('ix_message_between_from_user_id'), 'message_between', ['from_user_id'], unique=False)
    op.create_index(op.f('ix_message_between_order_id'), 'message_between', ['order_id'], unique=False)
    op.create_index(op.f('ix_message_between_to_user_id'), 'message_between', ['to_user_id'], unique=False)
    op.drop_index('ix_from_to_currency_count', table_name='order_request')
    op.create_index('ix_from_to_currency_count', 'order_request', ['from_currency', 'to_currency', 'min_limit_rub', 'max_limit_rub'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_from_to_currency_count', table_name='order_request')
    op.create_index('ix_from_to_currency_count', 'order_request', ['from_currency', 'to_currency', 'min_limit', 'max_limit'], unique=False)
    op.drop_index(op.f('ix_message_between_to_user_id'), table_name='message_between')
    op.drop_index(op.f('ix_message_between_order_id'), table_name='message_between')
    op.drop_index(op.f('ix_message_between_from_user_id'), table_name='message_between')
    op.drop_index(op.f('ix_message_between_created_at'), table_name='message_between')
    op.drop_table('message_between')
    # ### end Alembic commands ###
