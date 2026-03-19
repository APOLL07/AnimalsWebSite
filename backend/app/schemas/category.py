import uuid

from pydantic import BaseModel

from app.utils.localization import get_localized


class CategoryOut(BaseModel):
    id: uuid.UUID
    slug: str
    name: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_localized(cls, category, lang: str = "uk"):
        return cls(
            id=category.id,
            slug=category.slug,
            name=get_localized(category.name, lang),
        )


class CategoryTree(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    children: list["CategoryTree"] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_localized(cls, category, lang: str = "uk"):
        return cls(
            id=category.id,
            slug=category.slug,
            name=get_localized(category.name, lang),
            children=[
                cls.from_orm_localized(child, lang)
                for child in (category.children or [])
            ],
        )
