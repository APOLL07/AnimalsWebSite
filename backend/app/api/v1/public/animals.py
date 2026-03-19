from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.animal import Animal
from app.schemas.animal import AnimalOut

router = APIRouter()


@router.get("/", response_model=list[AnimalOut])
def list_animals(
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    animals = db.query(Animal).all()
    result = [AnimalOut.from_orm_localized(a, lang) for a in animals]
    result.sort(key=lambda a: a.name)
    return result
