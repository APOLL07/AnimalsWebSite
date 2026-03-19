"""Seed script: populates the database with initial data."""

import uuid

import bcrypt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401,F403
from app.models.admin_user import AdminUser
from app.models.animal import Animal
from app.models.category import Category


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

ANIMALS = [
    {"slug": "dogs", "name": "Собаки"},
    {"slug": "cats", "name": "Кошки"},
    {"slug": "rodents", "name": "Грызуны"},
    {"slug": "birds", "name": "Птицы"},
    {"slug": "fish", "name": "Рыбки"},
    {"slug": "reptiles", "name": "Рептилии"},
]

CATEGORIES = [
    {
        "slug": "food",
        "name": "Корма",
        "children": [
            {"slug": "dry-food", "name": "Сухой корм"},
            {"slug": "wet-food", "name": "Влажный корм"},
            {"slug": "treats", "name": "Лакомства"},
        ],
    },
    {
        "slug": "accessories",
        "name": "Амуниция",
        "children": [
            {"slug": "collars", "name": "Ошейники"},
            {"slug": "leashes", "name": "Поводки"},
            {"slug": "bowls", "name": "Миски"},
        ],
    },
    {
        "slug": "toys",
        "name": "Игрушки",
        "children": [],
    },
    {
        "slug": "health",
        "name": "Здоровье",
        "children": [
            {"slug": "vitamins", "name": "Витамины"},
            {"slug": "grooming", "name": "Груминг"},
        ],
    },
    {
        "slug": "housing",
        "name": "Жильё",
        "children": [
            {"slug": "beds", "name": "Лежанки"},
            {"slug": "cages", "name": "Клетки"},
            {"slug": "aquariums", "name": "Аквариумы"},
        ],
    },
]


def seed_animals(db: Session) -> None:
    for data in ANIMALS:
        existing = db.query(Animal).filter(Animal.slug == data["slug"]).first()
        if not existing:
            db.add(Animal(id=uuid.uuid4(), **data))
    db.commit()
    print(f"  Animals: {db.query(Animal).count()} records")


def seed_categories(db: Session) -> None:
    for cat_data in CATEGORIES:
        parent = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not parent:
            parent = Category(
                id=uuid.uuid4(),
                slug=cat_data["slug"],
                name=cat_data["name"],
                parent_id=None,
            )
            db.add(parent)
            db.flush()

        for child_data in cat_data.get("children", []):
            existing = db.query(Category).filter(Category.slug == child_data["slug"]).first()
            if not existing:
                db.add(
                    Category(
                        id=uuid.uuid4(),
                        slug=child_data["slug"],
                        name=child_data["name"],
                        parent_id=parent.id,
                    )
                )
    db.commit()
    print(f"  Categories: {db.query(Category).count()} records")


def seed_admin(db: Session) -> None:
    existing = db.query(AdminUser).filter(AdminUser.email == settings.ADMIN_EMAIL).first()
    if not existing:
        admin = AdminUser(
            id=uuid.uuid4(),
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print(f"  Admin user created: {settings.ADMIN_EMAIL}")
    else:
        print(f"  Admin user already exists: {settings.ADMIN_EMAIL}")


PRODUCTS = [
    {
        "slug": "royal-canin-maxi-adult",
        "name": "Royal Canin Maxi Adult",
        "brand": "Royal Canin",
        "description": "Сухой корм для крупных собак от 15 месяцев до 5 лет. Поддерживает здоровье суставов и оптимальный вес.",
        "animals": ["dogs"],
        "categories": ["food", "dry-food"],
        "attributes": [
            {"key": "Вес", "value": "15 кг", "is_main": True},
            {"key": "Возраст", "value": "от 15 месяцев", "is_main": True},
            {"key": "Страна", "value": "Франция", "is_main": False},
        ],
    },
    {
        "slug": "whiskas-tuna-pouch",
        "name": "Whiskas с тунцом в желе",
        "brand": "Whiskas",
        "description": "Влажный корм для взрослых кошек с нежным тунцом в аппетитном желе. Полнорационный.",
        "animals": ["cats"],
        "categories": ["food", "wet-food"],
        "attributes": [
            {"key": "Вес", "value": "85 г", "is_main": True},
            {"key": "Вкус", "value": "Тунец", "is_main": True},
        ],
    },
    {
        "slug": "ferplast-collar-ergocomfort",
        "name": "Ferplast Ergocomfort ошейник",
        "brand": "Ferplast",
        "description": "Эргономичный ошейник с мягкой подкладкой. Регулируемый размер, надёжная застёжка.",
        "animals": ["dogs"],
        "categories": ["accessories", "collars"],
        "attributes": [
            {"key": "Размер", "value": "M (34-42 см)", "is_main": True},
            {"key": "Цвет", "value": "Синий", "is_main": True},
            {"key": "Материал", "value": "Нейлон", "is_main": False},
        ],
    },
    {
        "slug": "kong-classic-red",
        "name": "KONG Classic игрушка",
        "brand": "KONG",
        "description": "Классическая игрушка из натурального каучука. Можно наполнять лакомствами. Отлично подходит для жевания.",
        "animals": ["dogs"],
        "categories": ["toys"],
        "attributes": [
            {"key": "Размер", "value": "L", "is_main": True},
            {"key": "Материал", "value": "Каучук", "is_main": True},
        ],
    },
    {
        "slug": "tetra-min-flakes",
        "name": "TetraMin основной корм хлопья",
        "brand": "Tetra",
        "description": "Основной корм в хлопьях для всех видов тропических рыб. Сбалансированная формула с витаминами.",
        "animals": ["fish"],
        "categories": ["food", "dry-food"],
        "attributes": [
            {"key": "Объём", "value": "250 мл", "is_main": True},
            {"key": "Тип", "value": "Хлопья", "is_main": True},
        ],
    },
    {
        "slug": "vitakraft-kracker-rodents",
        "name": "Vitakraft Kräcker для грызунов",
        "brand": "Vitakraft",
        "description": "Крекер-лакомство с мёдом и зерновыми для хомяков и морских свинок.",
        "animals": ["rodents"],
        "categories": ["food", "treats"],
        "attributes": [
            {"key": "Вес", "value": "112 г", "is_main": True},
            {"key": "Вкус", "value": "Мёд", "is_main": True},
        ],
    },
    {
        "slug": "trixie-bird-cage-natura",
        "name": "Trixie Natura клетка для птиц",
        "brand": "Trixie",
        "description": "Просторная клетка из натурального дерева для канареек и волнистых попугаев.",
        "animals": ["birds"],
        "categories": ["housing", "cages"],
        "attributes": [
            {"key": "Размер", "value": "60×40×80 см", "is_main": True},
            {"key": "Материал", "value": "Дерево/металл", "is_main": True},
        ],
    },
    {
        "slug": "exo-terra-terrarium-mini",
        "name": "Exo Terra террариум Mini",
        "brand": "Exo Terra",
        "description": "Компактный стеклянный террариум для небольших рептилий и амфибий. Передняя дверца для удобного доступа.",
        "animals": ["reptiles"],
        "categories": ["housing", "aquariums"],
        "attributes": [
            {"key": "Размер", "value": "30×30×30 см", "is_main": True},
            {"key": "Материал", "value": "Стекло", "is_main": True},
        ],
    },
    {
        "slug": "flexi-new-classic-leash",
        "name": "Flexi New Classic поводок-рулетка",
        "brand": "Flexi",
        "description": "Рулетка с тросовым поводком длиной 5 м. Надёжный тормозной механизм.",
        "animals": ["dogs"],
        "categories": ["accessories", "leashes"],
        "attributes": [
            {"key": "Длина", "value": "5 м", "is_main": True},
            {"key": "Макс. вес собаки", "value": "20 кг", "is_main": True},
        ],
    },
    {
        "slug": "8in1-excel-vitamins-adult",
        "name": "8in1 Excel мультивитамины",
        "brand": "8in1",
        "description": "Мультивитаминная добавка для взрослых собак. Содержит витамины группы B, антиоксиданты и минералы.",
        "animals": ["dogs"],
        "categories": ["health", "vitamins"],
        "attributes": [
            {"key": "Количество", "value": "70 таблеток", "is_main": True},
            {"key": "Возраст", "value": "Взрослые", "is_main": True},
        ],
    },
    {
        "slug": "furminator-deshedding-cat",
        "name": "FURminator дешеддер для кошек",
        "brand": "FURminator",
        "description": "Инструмент для удаления подшёрстка у короткошёрстных кошек. Снижает линьку до 90%.",
        "animals": ["cats"],
        "categories": ["health", "grooming"],
        "attributes": [
            {"key": "Тип шерсти", "value": "Короткая", "is_main": True},
            {"key": "Размер", "value": "S", "is_main": True},
        ],
    },
    {
        "slug": "trixie-cat-bed-minou",
        "name": "Trixie Minou лежанка",
        "brand": "Trixie",
        "description": "Мягкая плюшевая лежанка для кошек и маленьких собак. Бортики и подушка для максимального комфорта.",
        "animals": ["cats", "dogs"],
        "categories": ["housing", "beds"],
        "attributes": [
            {"key": "Размер", "value": "50×40 см", "is_main": True},
            {"key": "Материал", "value": "Плюш", "is_main": True},
            {"key": "Цвет", "value": "Бежевый", "is_main": False},
        ],
    },
]


def seed_products(db: Session) -> None:
    from app.models.product import ProductAttribute

    for data in PRODUCTS:
        existing = db.query(Product).filter(Product.slug == data["slug"]).first()
        if existing:
            continue

        product = Product(
            id=uuid.uuid4(),
            slug=data["slug"],
            name=data["name"],
            brand=data["brand"],
            description=data["description"],
            is_active=True,
        )

        animal_slugs = data.get("animals", [])
        if animal_slugs:
            animals = db.query(Animal).filter(Animal.slug.in_(animal_slugs)).all()
            product.animals = animals

        category_slugs = data.get("categories", [])
        if category_slugs:
            categories = db.query(Category).filter(Category.slug.in_(category_slugs)).all()
            product.categories = categories

        db.add(product)
        db.flush()

        for attr in data.get("attributes", []):
            db.add(ProductAttribute(
                id=uuid.uuid4(),
                product_id=product.id,
                key=attr["key"],
                value=attr["value"],
                is_main=attr.get("is_main", False),
            ))

    db.commit()
    print(f"  Products: {db.query(Product).count()} records")


def run_seeds() -> None:
    print("Seeding database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_animals(db)
        seed_categories(db)
        seed_admin(db)
        seed_products(db)
        print("Seeding complete!")
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
