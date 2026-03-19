import uuid

from pydantic import BaseModel

from app.utils.localization import get_localized


class AnimalOut(BaseModel):
    id: uuid.UUID
    slug: str
    name: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_localized(cls, animal, lang: str = "uk"):
        return cls(
            id=animal.id,
            slug=animal.slug,
            name=get_localized(animal.name, lang),
        )
