import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    parent: Mapped[Optional["Category"]] = relationship(
        back_populates="children",
        remote_side="Category.id",
        lazy="selectin",
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent",
        lazy="selectin",
    )
    products: Mapped[list["Product"]] = relationship(  # noqa: F821
        secondary="product_categories",
        back_populates="categories",
        lazy="selectin",
    )
