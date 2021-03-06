"""empty message

Revision ID: ebefe31cae94
Revises: b5ec14488f8d
Create Date: 2018-12-30 10:50:50.374256

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebefe31cae94'
down_revision = 'b5ec14488f8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memory', sa.Column('doc', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('memory', 'doc')
    # ### end Alembic commands ###
