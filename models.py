from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

# Parent class for all ORM models/tables
class Base(DeclarativeBase):
    pass

# Models for the database tables
class SampleMetadata(Base):
    # Maps class to the sample_metadata SQLite table
    __tablename__ = "sample_metadata"

    sample_id: Mapped[str] = mapped_column(String, primary_key=True)
    project: Mapped[str | None] = mapped_column(String)
    subject: Mapped[str | None] = mapped_column(String)
    condition: Mapped[str | None] = mapped_column(String)
    age: Mapped[int | None] = mapped_column(Integer)
    sex: Mapped[str | None] = mapped_column(String)
    treatment: Mapped[str | None] = mapped_column(String)
    response: Mapped[str | None] = mapped_column(String)
    sample_type: Mapped[str | None] = mapped_column(String)
    time_from_treatment_start: Mapped[int | None] = mapped_column(Integer)

    # Creates one-to-many relationship, allowing SampleMetadata objects to reference multiple CellCount objects
    counts: Mapped[list["CellCount"]] = relationship(back_populates="sample")

class CellCount(Base):
    # Maps class to the cell_counts SQLite table
    __tablename__ = "cell_counts"

    sample_id: Mapped[str] = mapped_column(ForeignKey("sample_metadata.sample_id", ondelete="CASCADE"), primary_key=True, index=True)
    cell_type: Mapped[str] = mapped_column(String, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)

    # Creates many-to-one relationship, allowing CellCount objects to reference sample info
    sample: Mapped[SampleMetadata] = relationship(back_populates="counts")