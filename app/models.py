import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from app.database import Base


class GenerationJob(Base):

    __tablename__ = "generation_jobs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    event_name = Column(
        String,
        nullable=False
    )

    course_name = Column(
        String,
        nullable=False
    )

    issue_date = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="PENDING"
    )

    total_count = Column(
        Integer,
        default=0
    )

    success_count = Column(
        Integer,
        default=0
    )

    failed_count = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    certificates = relationship(
        "Certificate",
        back_populates="job"
    )


class Certificate(Base):

    __tablename__ = "certificates"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    job_id = Column(
        String,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )

    recipient_name = Column(
        String,
        nullable=False
    )

    recipient_email = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="PENDING"
    )

    file_path = Column(
        String,
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    job = relationship(
        "GenerationJob",
        back_populates="certificates"
    )