from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.animal import Animal
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import PaginatedProducts, ProductDetail

router = APIRouter()


@router.get("/", response_model=PaginatedProducts)
def list_products(
    animal_slug: str | None = None,
    category_slug: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(name|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active.is_(True))

    if animal_slug:
        query = query.join(Product.animals).filter(Animal.slug == animal_slug)

    if category_slug:
        query = query.join(Product.categories).filter(Category.slug == category_slug)

    # JSONB-aware sorting
    if sort_by == "name":
        sort_column = Product.name[lang].astext
    else:
        sort_column = getattr(Product, sort_by)

    if sort_order == "desc":
        sort_column = sort_column.desc()

    total = query.count()
    items = query.order_by(sort_column).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedProducts(
        items=[ProductDetail.from_orm_localized(p, lang) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{slug}", response_model=ProductDetail)
def get_product(
    slug: str,
    lang: str = Query("uk", pattern="^(uk|ru)$"),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.slug == slug, Product.is_active.is_(True)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return ProductDetail.from_orm_localized(product, lang)
