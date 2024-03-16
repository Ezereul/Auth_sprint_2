"""history partition

Revision ID: 3
Revises: 2
Create Date: 2024-03-16 18:17:36.446031

"""
from datetime import date
from typing import Sequence, Union

from alembic import op
from dateutil.relativedelta import relativedelta
import sqlalchemy as sa

from auth.alembic.partition_utils import create_monthly_partitions


# revision identifiers, used by Alembic.
revision: str = '3'
down_revision: Union[str, None] = '2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    start_date = date(2024, 1, 1)
    end_date = date(2026, 1, 1)
    create_monthly_partitions(start_date, end_date)


def downgrade() -> None:
    start_date = date(2024, 1, 1)
    end_date = date(2026, 1, 1)
    current_date = start_date
    while current_date < end_date:
        partition_name = 'login_history_' + current_date.strftime('%Y_%m')
        op.execute(f"DROP TABLE IF EXISTS {partition_name};")
        current_date += relativedelta(months=+1)
