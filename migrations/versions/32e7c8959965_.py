"""empty message

Revision ID: 32e7c8959965
Revises: 16386380775b
Create Date: 2024-07-18 15:10:28.970911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32e7c8959965'
down_revision = '16386380775b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_album', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_album', schema=None) as batch_op:
        batch_op.drop_column('order')

    # ### end Alembic commands ###
