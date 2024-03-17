from sqlalchemy import UUID, Column, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import backref, relationship

from auth.src.core.db import Base


class SocialAccount(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref('social_accounts', lazy=True))

    social_id = Column(Text, nullable=False)
    social_name = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'