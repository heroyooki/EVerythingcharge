"""connections_autoincrement

Revision ID: 0019
Revises: 0018
Create Date: 2024-12-09 13:44:54.644001

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0019'
down_revision = '0018'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE connections_id_seq OWNED BY connections.id;")
    op.execute("ALTER TABLE connections ALTER COLUMN id SET DEFAULT nextval('connections_id_seq');")


def downgrade():
    op.execute("ALTER TABLE connections ALTER COLUMN id SET DEFAULT nextval('connections_id_seq');")
    op.execute("CREATE SEQUENCE connections_id_seq OWNED BY connections.id;")
