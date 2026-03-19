from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schemas.product import PaginatedProducts, ProductDetail

router = APIRouter()


@router.get("/", response_model=PaginatedProducts)
def search_products(
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    pattern = f"%{q}%"
    query = db.query(Product).filter(
        Product.is_active.is_(True),
        or_(
            Product.name[lang].astext.ilike(pattern),
            Product.brand.ilike(pattern),
            Product.description[lang].astext.ilike(pattern),
        ),
    )

    total = query.count()
    items = (
        query.order_by(Product.name[lang].astext)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedProducts(
        items=[ProductDetail.from_orm_localized(p, lang) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/suggest", response_model=list[ProductDetail])
def search_suggest(
    q: str = Query(..., min_length=1, max_length=200),
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    """Return up to 4 matching products for autocomplete."""
    pattern = f"%{q}%"
    items = (
        db.query(Product)
        .filter(
            Product.is_active.is_(True),
            or_(
                Product.name[lang].astext.ilike(pattern),
                Product.brand.ilike(pattern),
            ),
        )
        .order_by(Product.name[lang].astext)
        .limit(4)
        .all()
    )
    return [ProductDetail.from_orm_localized(p, lang) for p in items]
