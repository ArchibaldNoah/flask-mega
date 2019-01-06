"""empty message

Revision ID: 5d8fe36fcbb0
Revises: fce96335805d
Create Date: 2019-01-04 05:46:27.646080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d8fe36fcbb0'
down_revision = 'fce96335805d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memory_tag', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_memory_tag_timestamp'), 'memory_tag', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_memory_tag_timestamp'), table_name='memory_tag')
    op.drop_column('memory_tag', 'timestamp')
    # ### end Alembic commands ###
