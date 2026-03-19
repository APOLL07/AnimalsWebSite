from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryTree

router = APIRouter()


@router.get("/", response_model=list[CategoryTree])
def list_categories(db: Session = Depends(get_db)):
    roots = db.query(Category).filter(Category.parent_id.is_(None)).order_by(Category.name).all()
    return roots
