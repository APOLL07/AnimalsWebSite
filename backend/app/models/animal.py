import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[dict] = mapped_column(JSONB, nullable=False)

    products: Mapped[list["Product"]] = relationship(  # noqa: F821
        secondary="product_animals",
        back_populates="animals",
        lazy="selectin",
    )
