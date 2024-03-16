from datetime import date

from alembic import op
from dateutil.relativedelta import relativedelta


def create_monthly_partitions(start_date: date, end_date: date):
    current_date = start_date
    while current_date < end_date:
        partition_name = 'login_history_' + current_date.strftime('%Y_%m')
        partition_range_start = current_date.strftime('%Y-%m-%d')
        current_date += relativedelta(months=+1)
        partition_range_end = current_date.strftime('%Y-%m-%d')

        op.execute(f"""
            CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF loginhistory
            FOR VALUES FROM ('{partition_range_start}') TO ('{partition_range_end}');
        """)
