import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.animal import AnimalOut
from app.schemas.category import CategoryOut


class ProductImageOut(BaseModel):
    id: uuid.UUID
    url: str
    order: int
    is_main: bool
    media_type: str = "image"

    model_config = {"from_attributes": True}


class ProductAttributeOut(BaseModel):
    id: uuid.UUID
    key: str
    value: str
    is_main: bool

    model_config = {"from_attributes": True}


class ProductListItem(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    brand: str
    is_active: bool
    created_at: datetime
    main_image: ProductImageOut | None = None
    main_attributes: list[ProductAttributeOut] = []
    animals: list[AnimalOut] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_product(cls, product):
        main_image = next((img for img in product.images if img.is_main), None)
        if not main_image and product.images:
            main_image = product.images[0]
        main_attrs = [a for a in product.attributes if a.is_main]
        return cls(
            id=product.id,
            slug=product.slug,
            name=product.name,
            brand=product.brand,
            is_active=product.is_active,
            created_at=product.created_at,
            main_image=main_image,
            main_attributes=main_attrs,
            animals=product.animals,
        )


class ProductDetail(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    brand: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageOut] = []
    attributes: list[ProductAttributeOut] = []
    animals: list[AnimalOut] = []
    categories: list[CategoryOut] = []

    model_config = {"from_attributes": True}


class PaginatedProducts(BaseModel):
    items: list[ProductDetail] = []
    total: int
    page: int
    page_size: int
