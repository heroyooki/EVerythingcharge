"""connectors_table

Revision ID: 0007
Revises: 0006
Create Date: 2024-03-27 16:17:04.724579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('connectors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('error_code', sa.String(), nullable=True),
    sa.Column('charge_point_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['charge_point_id'], ['charge_points.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'charge_point_id'),
    sa.UniqueConstraint('id', 'charge_point_id')
    )
    op.create_index(op.f('ix_connectors_status'), 'connectors', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_connectors_status'), table_name='connectors')
    op.drop_table('connectors')
    # ### end Alembic commands ###
