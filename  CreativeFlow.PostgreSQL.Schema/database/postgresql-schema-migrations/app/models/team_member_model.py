import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from ..db.base import Base


class TeamMember(Base):
    """
    Junction table associating users with teams and their roles.
    """
    __tablename__ = 'team_members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    teamId = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(String(20), nullable=False, index=True)
    joinedAt = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

    __table_args__ = (
        UniqueConstraint('teamId', 'userId', name='uq_teammember_team_user'),
        CheckConstraint(role.in_(['Owner', 'Admin', 'Editor', 'Viewer']), name='ck_team_member_role'),
    )

    def __repr__(self):
        return f"<TeamMember(teamId='{self.teamId}', userId='{self.userId}', role='{self.role}')>"