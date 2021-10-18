"""empty message

Revision ID: c3c3a26ca827
Revises: 150016d49dda
Create Date: 2021-10-18 11:38:39.924387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c3a26ca827'
down_revision = '150016d49dda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('payment_intent', sa.String(), nullable=True))
    op.add_column('order', sa.Column('cancelled', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'order', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='unique')
    op.drop_column('order', 'cancelled')
    op.drop_column('order', 'payment_intent')
    # ### end Alembic commands ###