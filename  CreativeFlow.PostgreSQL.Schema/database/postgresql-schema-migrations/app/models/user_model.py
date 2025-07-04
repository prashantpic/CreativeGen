import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, DECIMAL, String, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from ..db.base import Base


class User(Base):
    """
    Represents a registered user account, storing authentication details,
    profile information, preferences, and links to user-specific data.
    """
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    passwordHash = Column(String(255), nullable=True)
    socialProvider = Column(String(50), nullable=True)
    socialProviderId = Column(String(255), nullable=True)
    isEmailVerified = Column(Boolean, nullable=False, default=False)
    emailVerificationToken = Column(String(255), nullable=True)
    passwordResetToken = Column(String(255), nullable=True)
    passwordResetExpires = Column(DateTime, nullable=True)
    fullName = Column(String(100), nullable=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    profilePictureUrl = Column(String(1024), nullable=True)
    languagePreference = Column(String(10), nullable=False, default='en-US', index=True)
    timezone = Column(String(50), nullable=False, default='UTC')
    mfaEnabled = Column(Boolean, nullable=False, default=False)
    mfaSecret = Column(String(255), nullable=True)
    subscriptionTier = Column(String(20), nullable=False, default='Free', index=True)
    creditBalance = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    lastLoginAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True, index=True)

    # Relationships
    brand_kits = relationship("BrandKit", back_populates="user", cascade="all, delete-orphan")
    workbenches = relationship("Workbench", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user")
    assets = relationship("Asset", back_populates="user")
    generation_requests = relationship("GenerationRequest", back_populates="user")
    social_media_connections = relationship("SocialMediaConnection", back_populates="user", cascade="all, delete-orphan")
    api_clients = relationship("APIClient", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    credit_transactions = relationship("CreditTransaction", back_populates="user")
    usage_logs = relationship("UsageLog", back_populates="user")
    owned_teams = relationship("Team", foreign_keys='Team.ownerId', back_populates="owner")
    team_memberships = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    created_templates = relationship("Template", back_populates="user_creator")
    ai_model_feedbacks = relationship("AIModelFeedback", back_populates="user")
    
    # Relationships for created/validated/deployed models
    created_model_versions = relationship("AIModelVersion", foreign_keys='AIModelVersion.createdByUserId')
    validated_model_results = relationship("AIModelValidationResult", foreign_keys='AIModelValidationResult.validatedByUserId')
    deployed_model_versions = relationship("AIModelDeployment", foreign_keys='AIModelDeployment.deployedByUserId')


    __table_args__ = (
        UniqueConstraint('socialProvider', 'socialProviderId', name='uq_user_social'),
        CheckConstraint(subscriptionTier.in_(['Free', 'Pro', 'Team', 'Enterprise']), name='ck_user_subscription_tier'),
        CheckConstraint(socialProvider.in_(['google', 'facebook', 'apple']), name='ck_user_social_provider'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"