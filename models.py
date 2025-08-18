from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class SampleMetadata(Base):
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

    counts: Mapped[list["CellCount"]] = relationship(back_populates="sample")

class CellCount(Base):
    __tablename__ = "cell_counts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(ForeignKey("sample_metadata.sample_id", ondelete="CASCADE"), index=True)
    cell_type: Mapped[str] = mapped_column(String)
    count: Mapped[int] = mapped_column(Integer)

    sample: Mapped[SampleMetadata] = relationship(back_populates="counts")