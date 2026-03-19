"""Admin schemas for product management."""

import uuid

from pydantic import BaseModel, Field


class AttributeIn(BaseModel):
    key: str = Field(max_length=100)
    value: str = Field(max_length=255)
    is_main: bool = False


class ProductCreate(BaseModel):
    name: str = Field(max_length=255)
    brand: str = Field(default="", max_length=100)
    description: str = ""
    is_active: bool = True
    animal_ids: list[uuid.UUID] = []
    category_ids: list[uuid.UUID] = []
    attributes: list[AttributeIn] = []


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    brand: str | None = Field(default=None, max_length=100)
    description: str | None = None
    is_active: bool | None = None
    animal_ids: list[uuid.UUID] | None = None
    category_ids: list[uuid.UUID] | None = None
    attributes: list[AttributeIn] | None = None


class ImageReorder(BaseModel):
    image_ids: list[uuid.UUID]


class AnimalCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: str | None = Field(default=None, max_length=100)


class AnimalUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    slug: str | None = Field(default=None, max_length=100)


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: str | None = Field(default=None, max_length=100)
    parent_id: uuid.UUID | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    slug: str | None = Field(default=None, max_length=100)
    parent_id: uuid.UUID | None = None
