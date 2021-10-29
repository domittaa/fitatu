"""menu table

Revision ID: bd08806f2d31
Revises: 55e055cd6d98
Create Date: 2021-10-29 09:41:25.004670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd08806f2d31'
down_revision = '55e055cd6d98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('products', sa.String(), nullable=True),
    sa.Column('calories', sa.Float(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    # ### end Alembic commands ###
