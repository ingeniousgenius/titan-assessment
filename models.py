from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime as SQLDateTime
from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.types import BigInteger

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True


class Tenant(BaseModel):
    """
    A tenant scopes all operations.

    design.rtf: Tenants: id (bigint), name (varchar(255))
    """

    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    logs: Mapped[list["ActivityLog"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    jobs: Mapped[list["AsyncJob"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")


class Book(BaseModel):
    """
    The logical "work" record, used by retrieval and as the parent for version snapshots.

    design.rtf: Books: id, tenant_id, title, author, first publish year, subjects jsonb array, cover image url
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True, nullable=False)

    # Needed to connect reading list submissions (which provide Open Library IDs or ISBNs)
    # back to a stable work record.
    work_identifier: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    first_publish_year: Mapped[int] = mapped_column(Integer, nullable=False)
    subjects: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(SQLDateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        SQLDateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="books")
    versions: Mapped[list["BookVersion"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (
        # Common retrieval filters/search should at least be indexable.
        Index("ix_books_tenant_title", "tenant_id", "title"),
        Index("ix_books_tenant_author", "tenant_id", "author"),
        Index("ix_books_tenant_year", "tenant_id", "first_publish_year"),
        # Avoid duplicate work rows when work_identifier is provided.
        Index("uq_books_tenant_work_identifier", "tenant_id", "work_identifier", unique=True),
    )


class BookVersion(BaseModel):
    """
    Append-only snapshot for version management.

    requirements.rtf:
    - create a new version rather than overwriting
    - track version history per work
    - handle regression (fields removed)
    """

    __tablename__ = "book_versions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)

    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_at: Mapped[datetime] = mapped_column(SQLDateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # "what changed" as a list of field names. Using JSONB keeps it flexible.
    changed_fields: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Snapshot fields (copy of Book metadata at the time of ingestion/refetch).
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    first_publish_year: Mapped[int] = mapped_column(Integer, nullable=False)
    subjects: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    book: Mapped["Book"] = relationship(back_populates="versions")

    __table_args__ = (
        # Ensure version numbers are unique per book.
        Index("uq_book_versions_book_version_number", "book_id", "version_number", unique=True),
        Index("ix_book_versions_book_version_at", "book_id", "version_at"),
    )

class ActivityLog(BaseModel):
    """
    Tier 1: record every ingestion operation and expose it via an API.

    requirements.rtf:
    - record requested (author/subject)
    - works fetched, succeeded, failed
    - timestamps
    - errors encountered
    """

    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True, nullable=False)
    log_data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default={})
    created_at: Mapped[datetime] = mapped_column(SQLDateTime(timezone=True), default=datetime.utcnow, nullable=False)

    tenant: Mapped["Tenant"] = relationship(back_populates="ingestion_logs")


class AsyncJob(BaseModel):
    """
    Tier 2: job queue/background processing.

    GraphQL design currently expects:
    - Query.jobStatus(jobId: String!): JobStatus!
    - Mutation endpoints returning AsynchronousJobResponse { jobId, status }
    """

    __tablename__ = "async_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True, nullable=False)

    # Use a string job id to match GraphQL `jobId: String` expectations.
    job_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    created_at: Mapped[datetime] = mapped_column(SQLDateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        SQLDateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Flexible payload for ingest inputs, reading list submissions, etc.
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    # Optional error message if status becomes FAILURE.
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="jobs")