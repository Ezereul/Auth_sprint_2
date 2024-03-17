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
    superuser_password_hash = pwd_context.hash('11111')
    superuser_role_id = '7c58fbfd-d77a-4ffa-8245-60e279ffe6b0'
    # INSERT INTO user ('id', 'username', 'password_hash', 'role_id')
    # VALUES ('338af451-398e-4bc0-9cde-394917bf1014', 'admin', '$argon2id$v=19$m=65536,t=3,p=4$mzNGyNlbyzknBGDsvRcihA$n2jQzY2ip0XERyddw7K2ypMvOUDGwjJsV2Bbptjf1Gk', '7c58fbfd-d77a-4ffa-8245-60e279ffe6b0');
    op.execute(
        r"INSERT INTO user ('id', 'username', 'password_hash', 'role_id') "
        "VALUES ('338af451-398e-4bc0-9cde-394917bf1014', 'admin', '{}', '{}');"
        .format(superuser_password_hash, superuser_role_id)
    )


def downgrade() -> None:
    op.execute(r"DELETE FROM user WHERE id='338af451-398e-4bc0-9cde-394917bf1014';")
