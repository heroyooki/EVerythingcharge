"""add_default_user

Revision ID: 0004
Revises: 0003
Create Date: 2024-03-24 10:46:06.152991

"""
from alembic import op

from app.web.users.service import get_password_context
from core.models import generate_default_id
from core.settings import (
    DEFAULT_USER_FIRST_NAME,
    DEFAULT_USER_LAST_NAME,
    DEFAULT_USER_LOGIN,
    DEFAULT_USER_PASSWORD
)

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    id = generate_default_id()
    password = get_password_context().hash(DEFAULT_USER_PASSWORD)

    op.execute(f"""
    INSERT INTO users (id, email, password, first_name, last_name) 
        VALUES ('{id}', '{DEFAULT_USER_LOGIN}', '{password}', '{DEFAULT_USER_FIRST_NAME}', '{DEFAULT_USER_LAST_NAME}');
    """)


def downgrade() -> None:
    op.execute("""
    DELETE FROM users WHERE email = 'admin@mail.com';
    """)
