"""delete calories column in menu table

Revision ID: 027ce0bffba4
Revises: 3eae224b33ee
Create Date: 2021-11-02 12:38:05.253142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '027ce0bffba4'
down_revision = '3eae224b33ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.drop_column('calories')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.add_column(sa.Column('calories', sa.FLOAT(), nullable=True))

    # ### end Alembic commands ###
