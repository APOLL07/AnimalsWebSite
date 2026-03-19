import uuid

from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: uuid.UUID
    slug: str
    name: str

    model_config = {"from_attributes": True}


class CategoryTree(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    children: list["CategoryTree"] = []

    model_config = {"from_attributes": True}
