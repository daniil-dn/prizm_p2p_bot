"""add withdraw referral

Revision ID: 5590e39779ae
Revises: bf9aef26e422
Create Date: 2025-03-24 22:17:11.257370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5590e39779ae'
down_revision = 'bf9aef26e422'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('withdraw_referral',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('summ', sa.Double(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_withdraw_referral_user_id'), 'withdraw_referral', ['user_id'], unique=False)
    op.add_column('user', sa.Column('referral_balance', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'referral_balance')
    op.drop_index(op.f('ix_withdraw_referral_user_id'), table_name='withdraw_referral')
    op.drop_table('withdraw_referral')
    # ### end Alembic commands ###
