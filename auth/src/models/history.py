from datetime import datetime, timedelta

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy import text, PrimaryKeyConstraint

from auth.src.core.db import Base


def create_monthly_partitions(engine, start_date: datetime, end_date: datetime):
    partition_format = "%Y%m"
    current_date = start_date
    while current_date < end_date:
        partition_name = f"login_history_{current_date.strftime(partition_format)}"
        partition_range_start = current_date.strftime("%Y-%m-%d")
        partition_range_end = (current_date + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

        sql = f"""
        CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF login_history
        FOR VALUES FROM ('{partition_range_start}') TO ('{partition_range_end}')
        """
        engine.execute(text(sql))

        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)


class LoginHistory(Base):
    __table_args__ = (PrimaryKeyConstraint('id', 'login_time'),
                      {'postgresql_partition_by': 'RANGE (login_time)'})

    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    login_time = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="login_history")
