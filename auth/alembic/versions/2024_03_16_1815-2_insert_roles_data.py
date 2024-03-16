"""insert roles data

Revision ID: 2
Revises: 1
Create Date: 2024-03-16 18:15:59.275330

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import table, column, String, Integer, UUID

from auth.src.core.constants import DEFAULT_ROLE_DATA, SUPERUSER_ROLE_DATA


# revision identifiers, used by Alembic.
revision: str = '2'
down_revision: Union[str, None] = '1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    roles_table = table('role',
        column('id', UUID),
        column('name', String),
        column('access_level', Integer),
    )
    op.bulk_insert(
        table=roles_table,
        rows=[
            {'id': '0eb8b11e-7a2a-421f-a792-6bab5cc9211a', **DEFAULT_ROLE_DATA},
            {'id': '7c58fbfd-d77a-4ffa-8245-60e279ffe6b0', **SUPERUSER_ROLE_DATA}
        ]
    )


def downgrade() -> None:
    op.execute(
        """UPDATE "user" SET role_id = NULL WHERE role_id IN (SELECT id FROM role WHERE name IN ('user', 'superuser'));""")
    op.execute("DELETE FROM role WHERE name IN ('user', 'superuser');")
