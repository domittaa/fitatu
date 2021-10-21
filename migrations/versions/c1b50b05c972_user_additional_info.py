"""user additional info

Revision ID: c1b50b05c972
Revises: 07f3daaa4d0c
Create Date: 2021-10-21 09:25:44.661065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1b50b05c972'
down_revision = '07f3daaa4d0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('weight', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('age', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'age')
    op.drop_column('user', 'sex')
    op.drop_column('user', 'height')
    op.drop_column('user', 'weight')
    # ### end Alembic commands ###