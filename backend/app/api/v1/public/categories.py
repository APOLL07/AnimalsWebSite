from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryTree

router = APIRouter()


@router.get("/", response_model=list[CategoryTree])
def list_categories(
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    roots = db.query(Category).filter(Category.parent_id.is_(None)).all()
    result = [CategoryTree.from_orm_localized(r, lang) for r in roots]
    result.sort(key=lambda c: c.name)
    return result
