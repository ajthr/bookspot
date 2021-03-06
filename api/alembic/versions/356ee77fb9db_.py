"""empty message

Revision ID: 356ee77fb9db
Revises: 34f4b6da9abb
Create Date: 2021-10-12 22:02:56.437245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '356ee77fb9db'
down_revision = '34f4b6da9abb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('copies', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'staff', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff', type_='unique')
    op.drop_column('product', 'copies')
    # ### end Alembic commands ###
