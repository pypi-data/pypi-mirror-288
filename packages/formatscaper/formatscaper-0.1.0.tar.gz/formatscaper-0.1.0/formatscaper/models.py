"""Data models for formatscaper."""

import dataclasses
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class ModelBase(DeclarativeBase):
    """Base class for models."""


@dataclasses.dataclass
class RecordFile:
    """Information about a file to be investigated."""

    filename: str
    uri: str
    record: str


@dataclasses.dataclass
class Format(ModelBase):
    """Information about a file format."""

    __tablename__ = "format"

    id: Mapped[int] = mapped_column(primary_key=True)
    puid: Mapped[Optional[str]] = mapped_column(unique=True)
    name: Mapped[Optional[str]] = mapped_column()
    mime: Mapped[Optional[str]] = mapped_column()

    # actually the probability of becoming obsolete, but that's quite a mouthful
    risk: Mapped[int] = mapped_column(default=0)

    results: Mapped[List["Result"]] = relationship(
        back_populates="format",
        cascade="all, delete-orphan",
    )
    comments: Mapped[List["FormatComment"]] = relationship(
        back_populates="format",
        cascade="all, delete-orphan",
    )

    def as_dict(self):
        """Dump the data as dictionary."""
        return {
            "puid": self.puid,
            "name": self.name,
            "mime": self.mime,
            "risk": self.risk,
        }

    @classmethod
    def from_sf_dict(cls, dictionary):
        """Parse the format from siegfried's output."""
        return cls(
            puid=dictionary["id"],
            name=dictionary["format"],
            mime=dictionary["mime"],
        )

    def __repr__(self):
        """Return repr(self) without the list of results."""
        return f"Format(puid='{self.puid}', name='{self.name}', mime='{self.mime}', risk={self.risk})"  # noqa


@dataclasses.dataclass
class FormatComment(ModelBase):
    """Comment about a file format."""

    __tablename__ = "format_comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str] = mapped_column()

    format_id: Mapped[Optional[int]] = mapped_column(ForeignKey("format.id"))
    format: Mapped[Format] = relationship(back_populates="comments")

    def __repr__(self):
        """Return repr(self)."""
        return f"FormatComment(comment='{self.comment}')"


@dataclasses.dataclass
class Result(ModelBase):
    """The format identification result for a given file."""

    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column()
    record: Mapped[Optional[str]] = mapped_column(default=None)
    impact: Mapped[int] = mapped_column(default=0)

    # flag indicating that the result was overridden manually
    overridden: Mapped[bool] = mapped_column(default=False)

    format_id: Mapped[Optional[int]] = mapped_column(ForeignKey("format.id"))
    format: Mapped[Format] = relationship(back_populates="results")

    # filenames are unique per record
    __table_args__ = (UniqueConstraint("record", "filename"),)

    @property
    def risk(self):
        """Calculate the risk assessment for the file."""
        return self.format.risk * self.impact

    def as_dict(self):
        """Dump the data as dictionary."""
        result = {
            "filename": self.filename,
            "record": self.record,
            "format": self.format.as_dict(),
            "impact": self.impact,
        }

        return result


def create_db_session(db_url: str = "sqlite://", create_tables: bool = True) -> Session:
    """Create a database session."""
    engine = create_engine(db_url)
    if create_tables:
        ModelBase.metadata.create_all(engine)

    return Session(engine)
