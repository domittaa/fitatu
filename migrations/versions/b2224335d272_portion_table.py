"""portion table

Revision ID: b2224335d272
Revises: 3a5ec6fdf9e7
Create Date: 2021-10-25 09:47:43.828839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2224335d272'
down_revision = '3a5ec6fdf9e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('portion', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('proteins', sa.Integer(), nullable=False),
    sa.Column('carbs', sa.Integer(), nullable=False),
    sa.Column('fats', sa.Integer(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portion')
    # ### end Alembic commands ###
