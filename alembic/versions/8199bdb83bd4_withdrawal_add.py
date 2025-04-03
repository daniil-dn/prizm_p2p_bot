"""withdrawal add

Revision ID: 8199bdb83bd4
Revises: 24ab8b831c31
Create Date: 2025-04-03 15:40:51.858587

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8199bdb83bd4'
down_revision = '24ab8b831c31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('withdrawal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False),
    sa.Column('commission_percent', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False),
    sa.Column('wallet', sa.String(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_withdrawal_created_at'), 'withdrawal', ['created_at'], unique=False)
    op.create_index(op.f('ix_withdrawal_user_id'), 'withdrawal', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_withdrawal_user_id'), table_name='withdrawal')
    op.drop_index(op.f('ix_withdrawal_created_at'), table_name='withdrawal')
    op.drop_table('withdrawal')
    # ### end Alembic commands ###
