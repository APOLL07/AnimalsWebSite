"""Admin CRUD endpoints for products, images, animals, and categories."""

import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.admin_user import AdminUser
from app.models.animal import Animal
from app.models.category import Category
from app.models.product import Product, ProductAttribute, ProductImage
from app.schemas.admin import (
    AnimalCreate,
    AnimalUpdate,
    CategoryCreate,
    CategoryUpdate,
    ImageReorder,
    ProductCreate,
    ProductUpdate,
)
from app.schemas.animal import AnimalOut
from app.schemas.category import CategoryTree
from app.schemas.product import ProductDetail
from app.security.dependencies import get_current_admin
from app.services.images import delete_image_files, delete_video_file, save_upload, save_video_upload
from app.services.slug import generate_slug


def _make_slug(name: str) -> str:
    """Simple slug from name (transliterate Russian)."""
    from app.services.slug import _transliterate

    base = _transliterate(name)
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")

router = APIRouter()


@router.post("/products", response_model=ProductDetail, status_code=status.HTTP_201_CREATED)
async def create_product(
    body: ProductCreate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    slug = generate_slug(body.name, db)
    product = Product(
        id=uuid.uuid4(),
        slug=slug,
        name=body.name,
        brand=body.brand,
        description=body.description,
        is_active=body.is_active,
    )

    if body.animal_ids:
        animals = db.query(Animal).filter(Animal.id.in_(body.animal_ids)).all()
        product.animals = animals

    if body.category_ids:
        categories = db.query(Category).filter(Category.id.in_(body.category_ids)).all()
        product.categories = categories

    for attr in body.attributes:
        product.attributes.append(
            ProductAttribute(id=uuid.uuid4(), key=attr.key, value=attr.value, is_main=attr.is_main)
        )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/products/{product_id}", response_model=ProductDetail)
async def update_product(
    product_id: uuid.UUID,
    body: ProductUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if body.name is not None:
        product.name = body.name
    if body.brand is not None:
        product.brand = body.brand
    if body.description is not None:
        product.description = body.description
    if body.is_active is not None:
        product.is_active = body.is_active

    if body.animal_ids is not None:
        animals = db.query(Animal).filter(Animal.id.in_(body.animal_ids)).all()
        product.animals = animals

    if body.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(body.category_ids)).all()
        product.categories = categories

    if body.attributes is not None:
        for old_attr in product.attributes:
            db.delete(old_attr)
        db.flush()
        for attr in body.attributes:
            product.attributes.append(
                ProductAttribute(id=uuid.uuid4(), key=attr.key, value=attr.value, is_main=attr.is_main)
            )

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    for img in product.images:
        delete_image_files(img.url)

    db.delete(product)
    db.commit()


@router.post("/products/{product_id}/images", response_model=ProductDetail)
async def upload_image(
    product_id: uuid.UUID,
    file: UploadFile,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if len(product.images) >= settings.MAX_IMAGES_PER_PRODUCT:
        raise HTTPException(status_code=400, detail="Достигнут лимит изображений")

    urls = await save_upload(file)
    is_main = len(product.images) == 0
    order = max((img.order for img in product.images), default=-1) + 1

    image = ProductImage(
        id=uuid.uuid4(),
        product_id=product.id,
        url=urls["large"],
        order=order,
        is_main=is_main,
    )
    db.add(image)
    db.commit()
    db.refresh(product)
    return product


@router.post("/products/{product_id}/videos", response_model=ProductDetail)
async def upload_video(
    product_id: uuid.UUID,
    file: UploadFile,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    url = await save_video_upload(file)
    order = max((img.order for img in product.images), default=-1) + 1

    media = ProductImage(
        id=uuid.uuid4(),
        product_id=product.id,
        url=url,
        order=order,
        is_main=False,
        media_type="video",
    )
    db.add(media)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    if image.media_type == "video":
        delete_video_file(image.url)
    else:
        delete_image_files(image.url)
    db.delete(image)
    db.commit()


@router.put("/products/{product_id}/images/reorder", response_model=ProductDetail)
async def reorder_images(
    product_id: uuid.UUID,
    body: ImageReorder,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    image_map = {img.id: img for img in product.images}
    for idx, img_id in enumerate(body.image_ids):
        if img_id in image_map:
            image_map[img_id].order = idx
            image_map[img_id].is_main = idx == 0

    db.commit()
    db.refresh(product)
    return product


# ── Animal CRUD ──────────────────────────────────────────────


@router.post("/animals", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
async def create_animal(
    body: AnimalCreate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    slug = body.slug or _make_slug(body.name)
    if db.query(Animal).filter(Animal.slug == slug).first():
        raise HTTPException(status_code=400, detail="Животное с таким slug уже существует")
    animal = Animal(id=uuid.uuid4(), slug=slug, name=body.name)
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@router.patch("/animals/{animal_id}", response_model=AnimalOut)
async def update_animal(
    animal_id: uuid.UUID,
    body: AnimalUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Животное не найдено")
    if body.name is not None:
        animal.name = body.name
    if body.slug is not None:
        if db.query(Animal).filter(Animal.slug == body.slug, Animal.id != animal_id).first():
            raise HTTPException(status_code=400, detail="Этот slug уже занят")
        animal.slug = body.slug
    db.commit()
    db.refresh(animal)
    return animal


@router.delete("/animals/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Животное не найдено")
    db.delete(animal)
    db.commit()


# ── Category CRUD ────────────────────────────────────────────


@router.post("/categories", response_model=CategoryTree, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CategoryCreate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    slug = body.slug or _make_slug(body.name)
    if db.query(Category).filter(Category.slug == slug).first():
        raise HTTPException(status_code=400, detail="Категория с таким slug уже существует")
    if body.parent_id:
        parent = db.query(Category).filter(Category.id == body.parent_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Родительская категория не найдена")
    cat = Category(id=uuid.uuid4(), slug=slug, name=body.name, parent_id=body.parent_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.patch("/categories/{category_id}", response_model=CategoryTree)
async def update_category(
    category_id: uuid.UUID,
    body: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    if body.name is not None:
        cat.name = body.name
    if body.slug is not None:
        if db.query(Category).filter(Category.slug == body.slug, Category.id != category_id).first():
            raise HTTPException(status_code=400, detail="Этот slug уже занят")
        cat.slug = body.slug
    if body.parent_id is not None:
        cat.parent_id = body.parent_id
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    db.delete(cat)
    db.commit()
