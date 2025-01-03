"""components_and_variables_tables

Revision ID: 0002
Revises: 0001
Create Date: 2024-12-10 10:47:18.224876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('components',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('parent_id', sa.String(), nullable=True),
    sa.Column('master_id', sa.String(length=36), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['components.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_components_id'), 'components', ['id'], unique=True)
    op.create_table('variables',
    sa.Column('component_id', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_variables_id'), 'variables', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_variables_id'), table_name='variables')
    op.drop_table('variables')
    op.drop_index(op.f('ix_components_id'), table_name='components')
    op.drop_table('components')
    # ### end Alembic commands ###
