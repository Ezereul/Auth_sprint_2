"""create superuser

Revision ID: 4
Revises: 3
Create Date: 2024-03-17 15:53:30.307566

"""
from typing import Sequence, Union

from alembic import op

from auth.src.models.user import pwd_context

# revision identifiers, used by Alembic.
revision: str = '4'
down_revision: Union[str, None] = '3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    query = (r"INSERT INTO public.user (id, username, password_hash, role_id) "  # noqa
             r"VALUES ('{id}', '{username}', '{password_hash}', '{role_id}');")

    superuser_password = '11111'
    superuser_data = {
        'id': '338af451-398e-4bc0-9cde-394917bf1014',
        'username': 'admin',
        'password_hash': pwd_context.hash(superuser_password),
        'role_id': '7c58fbfd-d77a-4ffa-8245-60e279ffe6b0',
    }

    op.execute(query.format(**superuser_data))


def downgrade() -> None:
    op.execute(r"DELETE FROM public.user WHERE id='338af451-398e-4bc0-9cde-394917bf1014';")
