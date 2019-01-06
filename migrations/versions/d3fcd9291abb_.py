"""empty message

Revision ID: d3fcd9291abb
Revises: 5d8fe36fcbb0
Create Date: 2019-01-05 14:25:09.004786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3fcd9291abb'
down_revision = '5d8fe36fcbb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memory', sa.Column('dormant', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('memory', 'dormant')
    # ### end Alembic commands ###
