import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductAnimal(Base):
    __tablename__ = "product_animals"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    animal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("animals.id", ondelete="CASCADE"), primary_key=True
    )


class ProductCategory(Base):
    __tablename__ = "product_categories"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    )
