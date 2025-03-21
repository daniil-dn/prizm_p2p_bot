"""update orders

Revision ID: 1fb2467c77fc
Revises: f9cf0e751a9e
Create Date: 2025-03-07 01:56:40.381656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb2467c77fc'
down_revision = 'f9cf0e751a9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('prizm_value', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False))
    op.add_column('order', sa.Column('rub_value', sa.Numeric(precision=18, scale=4, asdecimal=False), nullable=False))
    op.drop_column('order', 'to_value')
    op.drop_column('order', 'from_value')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('from_value', sa.NUMERIC(precision=18, scale=4), autoincrement=False, nullable=False))
    op.add_column('order', sa.Column('to_value', sa.NUMERIC(precision=18, scale=4), autoincrement=False, nullable=False))
    op.drop_column('order', 'rub_value')
    op.drop_column('order', 'prizm_value')
    # ### end Alembic commands ###
