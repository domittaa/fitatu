"""fridge table

Revision ID: 699b657e937e
Revises: 03acea59b3f7
Create Date: 2021-10-27 11:41:00.863811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '699b657e937e'
down_revision = '03acea59b3f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fridge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('expired_date', sa.Date(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fridge')
    # ### end Alembic commands ###
