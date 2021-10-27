"""Add user_id to shopping table

Revision ID: 03acea59b3f7
Revises: a92feb44195c
Create Date: 2021-10-27 08:13:35.579863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03acea59b3f7'
down_revision = 'a92feb44195c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shopping', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_user_id_id', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shopping', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_user_id_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
