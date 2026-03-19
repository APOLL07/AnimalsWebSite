"""Admin schemas for product management."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.product import ProductImageOut


# ── Admin input schemas ──────────────────────────────────────


class AttributeIn(BaseModel):
    key: dict[str, str] = Field(default_factory=dict)
    value: dict[str, str] = Field(default_factory=dict)
    is_main: bool = False


class ProductCreate(BaseModel):
    name: dict[str, str] = Field(default_factory=dict)
    brand: str = Field(default="", max_length=100)
    description: dict[str, str] = Field(default_factory=dict)
    is_active: bool = True
    animal_ids: list[uuid.UUID] = []
    category_ids: list[uuid.UUID] = []
    attributes: list[AttributeIn] = []


class ProductUpdate(BaseModel):
    name: dict[str, str] | None = None
    brand: str | None = Field(default=None, max_length=100)
    description: dict[str, str] | None = None
    is_active: bool | None = None
    animal_ids: list[uuid.UUID] | None = None
    category_ids: list[uuid.UUID] | None = None
    attributes: list[AttributeIn] | None = None


class ImageReorder(BaseModel):
    image_ids: list[uuid.UUID]


class AnimalCreate(BaseModel):
    name: dict[str, str] = Field(default_factory=dict)
    slug: str | None = Field(default=None, max_length=100)


class AnimalUpdate(BaseModel):
    name: dict[str, str] | None = None
    slug: str | None = Field(default=None, max_length=100)


class CategoryCreate(BaseModel):
    name: dict[str, str] = Field(default_factory=dict)
    slug: str | None = Field(default=None, max_length=100)
    parent_id: uuid.UUID | None = None


class CategoryUpdate(BaseModel):
    name: dict[str, str] | None = None
    slug: str | None = Field(default=None, max_length=100)
    parent_id: uuid.UUID | None = None


# ── Admin response schemas (return full JSONB) ───────────────


class ProductAttributeAdmin(BaseModel):
    id: uuid.UUID
    key: dict
    value: dict
    is_main: bool

    model_config = {"from_attributes": True}


class AnimalOutAdmin(BaseModel):
    id: uuid.UUID
    slug: str
    name: dict

    model_config = {"from_attributes": True}


class CategoryOutAdmin(BaseModel):
    id: uuid.UUID
    slug: str
    name: dict

    model_config = {"from_attributes": True}


class CategoryTreeAdmin(BaseModel):
    id: uuid.UUID
    slug: str
    name: dict
    children: list["CategoryTreeAdmin"] = []

    model_config = {"from_attributes": True}


class ProductDetailAdmin(BaseModel):
    id: uuid.UUID
    slug: str
    name: dict
    brand: str
    description: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageOut] = []
    attributes: list[ProductAttributeAdmin] = []
    animals: list[AnimalOutAdmin] = []
    categories: list[CategoryOutAdmin] = []

    model_config = {"from_attributes": True}
