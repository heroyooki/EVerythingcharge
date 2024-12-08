"""common_connections_table

Revision ID: 0014
Revises: 0013
Create Date: 2024-12-06 11:17:01.613873

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0014'
down_revision = '0013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('connectors_evse_id_fkey', 'connectors', type_='foreignkey')
    op.alter_column('evses', 'id',
                    existing_type=sa.SMALLINT(),
                    type_=sa.String(length=20),
                    existing_nullable=False,
                    existing_server_default=sa.text("nextval('evses_id_seq'::regclass)"))
    op.alter_column('connectors', 'evse_id',
                    existing_type=sa.SMALLINT(),
                    type_=sa.String(),
                    existing_nullable=False)
    op.alter_column('connectors', 'id',
                    existing_type=sa.SMALLINT(),
                    type_=sa.String(length=20),
                    existing_nullable=False)
    op.create_foreign_key(None, 'connectors', 'evses', ['evse_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('evses', 'id',
                    existing_type=sa.String(length=20),
                    type_=sa.SMALLINT(),
                    existing_nullable=False,
                    existing_server_default=sa.text("nextval('evses_id_seq'::regclass)"))
    op.alter_column('connectors', 'evse_id',
                    existing_type=sa.String(),
                    type_=sa.SMALLINT(),
                    existing_nullable=False)
    op.alter_column('connectors', 'id',
                    existing_type=sa.String(length=20),
                    type_=sa.SMALLINT(),
                    existing_nullable=False)
    # ### end Alembic commands ###