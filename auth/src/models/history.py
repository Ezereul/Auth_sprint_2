import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy import text, PrimaryKeyConstraint

from auth.src.core.db import Base


class LoginHistory(Base):
    __table_args__ = (PrimaryKeyConstraint('id', 'login_time'),
                      {'postgresql_partition_by': 'RANGE (login_time)'})

    id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    login_time = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="login_history")
