from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.animal import Animal
from app.schemas.animal import AnimalOut

router = APIRouter()


@router.get("/", response_model=list[AnimalOut])
def list_animals(db: Session = Depends(get_db)):
    return db.query(Animal).order_by(Animal.name).all()
