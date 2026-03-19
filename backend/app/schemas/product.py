import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.animal import AnimalOut
from app.schemas.category import CategoryOut
from app.utils.localization import get_localized


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

    @classmethod
    def from_orm_localized(cls, attr, lang: str = "uk"):
        return cls(
            id=attr.id,
            key=get_localized(attr.key, lang),
            value=get_localized(attr.value, lang),
            is_main=attr.is_main,
        )


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
    def from_product(cls, product, lang: str = "uk"):
        main_image = next((img for img in product.images if img.is_main), None)
        if not main_image and product.images:
            main_image = product.images[0]
        main_attrs = [
            ProductAttributeOut.from_orm_localized(a, lang)
            for a in product.attributes if a.is_main
        ]
        return cls(
            id=product.id,
            slug=product.slug,
            name=get_localized(product.name, lang),
            brand=product.brand,
            is_active=product.is_active,
            created_at=product.created_at,
            main_image=main_image,
            main_attributes=main_attrs,
            animals=[AnimalOut.from_orm_localized(a, lang) for a in product.animals],
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

    @classmethod
    def from_orm_localized(cls, product, lang: str = "uk"):
        return cls(
            id=product.id,
            slug=product.slug,
            name=get_localized(product.name, lang),
            brand=product.brand,
            description=get_localized(product.description, lang),
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
            images=[ProductImageOut.model_validate(img, from_attributes=True) for img in product.images],
            attributes=[ProductAttributeOut.from_orm_localized(a, lang) for a in product.attributes],
            animals=[AnimalOut.from_orm_localized(a, lang) for a in product.animals],
            categories=[CategoryOut.from_orm_localized(c, lang) for c in product.categories],
        )


class PaginatedProducts(BaseModel):
    items: list[ProductDetail] = []
    total: int
    page: int
    page_size: int
