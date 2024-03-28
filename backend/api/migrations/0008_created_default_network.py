"""created_default_network

Revision ID: 0008
Revises: 0007
Create Date: 2024-03-28 20:52:05.681593

"""
from alembic import op

from core.models import generate_default_id

# revision identifiers, used by Alembic.
revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    id = generate_default_id()

    op.execute(f"""
    INSERT INTO networks (id, name, location) 
        VALUES ('{id}', 'Main', 'Office');
    """)


def downgrade() -> None:
    op.execute("""
    DELETE FROM networks WHERE name = 'Main';
    """)
