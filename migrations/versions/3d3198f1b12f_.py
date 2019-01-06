"""empty message

Revision ID: 3d3198f1b12f
Revises: ebefe31cae94
Create Date: 2018-12-30 15:47:59.786193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d3198f1b12f'
down_revision = 'ebefe31cae94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('tag', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_tag'), 'tag', ['tag'], unique=False)
    op.create_index(op.f('ix_tag_timestamp'), 'tag', ['timestamp'], unique=False)
    op.create_table('memory_tag',
    sa.Column('memory_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['memory_id'], ['memory.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('memory_id', 'tag_id')
    )
    op.add_column('memory', sa.Column('abstract', sa.String(length=256), nullable=True))
    op.add_column('memory', sa.Column('category', sa.String(length=32), nullable=True))
    op.add_column('memory', sa.Column('type', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_memory_category'), 'memory', ['category'], unique=False)
    op.create_index(op.f('ix_memory_type'), 'memory', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_memory_type'), table_name='memory')
    op.drop_index(op.f('ix_memory_category'), table_name='memory')
    op.drop_column('memory', 'type')
    op.drop_column('memory', 'category')
    op.drop_column('memory', 'abstract')
    op.drop_table('memory_tag')
    op.drop_index(op.f('ix_tag_timestamp'), table_name='tag')
    op.drop_index(op.f('ix_tag_tag'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###
