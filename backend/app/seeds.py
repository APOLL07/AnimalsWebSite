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
    {"slug": "dogs", "name": {"uk": "Собаки", "ru": "Собаки"}},
    {"slug": "cats", "name": {"uk": "Коти", "ru": "Кошки"}},
    {"slug": "rodents", "name": {"uk": "Гризуни", "ru": "Грызуны"}},
    {"slug": "birds", "name": {"uk": "Птахи", "ru": "Птицы"}},
    {"slug": "fish", "name": {"uk": "Рибки", "ru": "Рыбки"}},
    {"slug": "reptiles", "name": {"uk": "Рептилії", "ru": "Рептилии"}},
]

CATEGORIES = [
    {
        "slug": "food",
        "name": {"uk": "Корми", "ru": "Корма"},
        "children": [
            {"slug": "dry-food", "name": {"uk": "Сухий корм", "ru": "Сухой корм"}},
            {"slug": "wet-food", "name": {"uk": "Вологий корм", "ru": "Влажный корм"}},
            {"slug": "treats", "name": {"uk": "Ласощі", "ru": "Лакомства"}},
        ],
    },
    {
        "slug": "accessories",
        "name": {"uk": "Амуніція", "ru": "Амуниция"},
        "children": [
            {"slug": "collars", "name": {"uk": "Нашийники", "ru": "Ошейники"}},
            {"slug": "leashes", "name": {"uk": "Повідки", "ru": "Поводки"}},
            {"slug": "bowls", "name": {"uk": "Миски", "ru": "Миски"}},
        ],
    },
    {
        "slug": "toys",
        "name": {"uk": "Іграшки", "ru": "Игрушки"},
        "children": [],
    },
    {
        "slug": "health",
        "name": {"uk": "Здоров'я", "ru": "Здоровье"},
        "children": [
            {"slug": "vitamins", "name": {"uk": "Вітаміни", "ru": "Витамины"}},
            {"slug": "grooming", "name": {"uk": "Грумінг", "ru": "Груминг"}},
        ],
    },
    {
        "slug": "housing",
        "name": {"uk": "Житло", "ru": "Жильё"},
        "children": [
            {"slug": "beds", "name": {"uk": "Лежанки", "ru": "Лежанки"}},
            {"slug": "cages", "name": {"uk": "Клітки", "ru": "Клетки"}},
            {"slug": "aquariums", "name": {"uk": "Акваріуми", "ru": "Аквариумы"}},
        ],
    },
]


def seed_animals(db: Session) -> None:
    for data in ANIMALS:
        existing = db.query(Animal).filter(Animal.slug == data["slug"]).first()
        if not existing:
            db.add(Animal(id=uuid.uuid4(), **data))
        else:
            existing.name = data["name"]
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
        else:
            parent.name = cat_data["name"]

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
            else:
                existing.name = child_data["name"]
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
        "name": {"uk": "Royal Canin Maxi Adult", "ru": "Royal Canin Maxi Adult"},
        "brand": "Royal Canin",
        "description": {
            "uk": "Сухий корм для великих собак від 15 місяців до 5 років. Підтримує здоров'я суглобів та оптимальну вагу.",
            "ru": "Сухой корм для крупных собак от 15 месяцев до 5 лет. Поддерживает здоровье суставов и оптимальный вес.",
        },
        "animals": ["dogs"],
        "categories": ["food", "dry-food"],
        "attributes": [
            {"key": {"uk": "Вага", "ru": "Вес"}, "value": {"uk": "15 кг", "ru": "15 кг"}, "is_main": True},
            {"key": {"uk": "Вік", "ru": "Возраст"}, "value": {"uk": "від 15 місяців", "ru": "от 15 месяцев"}, "is_main": True},
            {"key": {"uk": "Країна", "ru": "Страна"}, "value": {"uk": "Франція", "ru": "Франция"}, "is_main": False},
        ],
    },
    {
        "slug": "whiskas-tuna-pouch",
        "name": {"uk": "Whiskas з тунцем у желе", "ru": "Whiskas с тунцом в желе"},
        "brand": "Whiskas",
        "description": {
            "uk": "Вологий корм для дорослих котів з ніжним тунцем в апетитному желе. Повнораціонний.",
            "ru": "Влажный корм для взрослых кошек с нежным тунцом в аппетитном желе. Полнорационный.",
        },
        "animals": ["cats"],
        "categories": ["food", "wet-food"],
        "attributes": [
            {"key": {"uk": "Вага", "ru": "Вес"}, "value": {"uk": "85 г", "ru": "85 г"}, "is_main": True},
            {"key": {"uk": "Смак", "ru": "Вкус"}, "value": {"uk": "Тунець", "ru": "Тунец"}, "is_main": True},
        ],
    },
    {
        "slug": "ferplast-collar-ergocomfort",
        "name": {"uk": "Ferplast Ergocomfort нашийник", "ru": "Ferplast Ergocomfort ошейник"},
        "brand": "Ferplast",
        "description": {
            "uk": "Ергономічний нашийник з м'якою підкладкою. Регульований розмір, надійна застібка.",
            "ru": "Эргономичный ошейник с мягкой подкладкой. Регулируемый размер, надёжная застёжка.",
        },
        "animals": ["dogs"],
        "categories": ["accessories", "collars"],
        "attributes": [
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "M (34-42 см)", "ru": "M (34-42 см)"}, "is_main": True},
            {"key": {"uk": "Колір", "ru": "Цвет"}, "value": {"uk": "Синій", "ru": "Синий"}, "is_main": True},
            {"key": {"uk": "Матеріал", "ru": "Материал"}, "value": {"uk": "Нейлон", "ru": "Нейлон"}, "is_main": False},
        ],
    },
    {
        "slug": "kong-classic-red",
        "name": {"uk": "KONG Classic іграшка", "ru": "KONG Classic игрушка"},
        "brand": "KONG",
        "description": {
            "uk": "Класична іграшка з натурального каучуку. Можна наповнювати ласощами. Чудово підходить для жування.",
            "ru": "Классическая игрушка из натурального каучука. Можно наполнять лакомствами. Отлично подходит для жевания.",
        },
        "animals": ["dogs"],
        "categories": ["toys"],
        "attributes": [
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "L", "ru": "L"}, "is_main": True},
            {"key": {"uk": "Матеріал", "ru": "Материал"}, "value": {"uk": "Каучук", "ru": "Каучук"}, "is_main": True},
        ],
    },
    {
        "slug": "tetra-min-flakes",
        "name": {"uk": "TetraMin основний корм пластівці", "ru": "TetraMin основной корм хлопья"},
        "brand": "Tetra",
        "description": {
            "uk": "Основний корм у пластівцях для всіх видів тропічних риб. Збалансована формула з вітамінами.",
            "ru": "Основной корм в хлопьях для всех видов тропических рыб. Сбалансированная формула с витаминами.",
        },
        "animals": ["fish"],
        "categories": ["food", "dry-food"],
        "attributes": [
            {"key": {"uk": "Об'єм", "ru": "Объём"}, "value": {"uk": "250 мл", "ru": "250 мл"}, "is_main": True},
            {"key": {"uk": "Тип", "ru": "Тип"}, "value": {"uk": "Пластівці", "ru": "Хлопья"}, "is_main": True},
        ],
    },
    {
        "slug": "vitakraft-kracker-rodents",
        "name": {"uk": "Vitakraft Kräcker для гризунів", "ru": "Vitakraft Kräcker для грызунов"},
        "brand": "Vitakraft",
        "description": {
            "uk": "Крекер-ласощі з медом та зерновими для хом'яків та морських свинок.",
            "ru": "Крекер-лакомство с мёдом и зерновыми для хомяков и морских свинок.",
        },
        "animals": ["rodents"],
        "categories": ["food", "treats"],
        "attributes": [
            {"key": {"uk": "Вага", "ru": "Вес"}, "value": {"uk": "112 г", "ru": "112 г"}, "is_main": True},
            {"key": {"uk": "Смак", "ru": "Вкус"}, "value": {"uk": "Мед", "ru": "Мёд"}, "is_main": True},
        ],
    },
    {
        "slug": "trixie-bird-cage-natura",
        "name": {"uk": "Trixie Natura клітка для птахів", "ru": "Trixie Natura клетка для птиц"},
        "brand": "Trixie",
        "description": {
            "uk": "Простора клітка з натурального дерева для канарок та хвилястих папуг.",
            "ru": "Просторная клетка из натурального дерева для канареек и волнистых попугаев.",
        },
        "animals": ["birds"],
        "categories": ["housing", "cages"],
        "attributes": [
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "60×40×80 см", "ru": "60×40×80 см"}, "is_main": True},
            {"key": {"uk": "Матеріал", "ru": "Материал"}, "value": {"uk": "Дерево/метал", "ru": "Дерево/металл"}, "is_main": True},
        ],
    },
    {
        "slug": "exo-terra-terrarium-mini",
        "name": {"uk": "Exo Terra тераріум Mini", "ru": "Exo Terra террариум Mini"},
        "brand": "Exo Terra",
        "description": {
            "uk": "Компактний скляний тераріум для невеликих рептилій та амфібій. Передні дверцята для зручного доступу.",
            "ru": "Компактный стеклянный террариум для небольших рептилий и амфибий. Передняя дверца для удобного доступа.",
        },
        "animals": ["reptiles"],
        "categories": ["housing", "aquariums"],
        "attributes": [
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "30×30×30 см", "ru": "30×30×30 см"}, "is_main": True},
            {"key": {"uk": "Матеріал", "ru": "Материал"}, "value": {"uk": "Скло", "ru": "Стекло"}, "is_main": True},
        ],
    },
    {
        "slug": "flexi-new-classic-leash",
        "name": {"uk": "Flexi New Classic повідок-рулетка", "ru": "Flexi New Classic поводок-рулетка"},
        "brand": "Flexi",
        "description": {
            "uk": "Рулетка з тросовим повідком довжиною 5 м. Надійний гальмівний механізм.",
            "ru": "Рулетка с тросовым поводком длиной 5 м. Надёжный тормозной механизм.",
        },
        "animals": ["dogs"],
        "categories": ["accessories", "leashes"],
        "attributes": [
            {"key": {"uk": "Довжина", "ru": "Длина"}, "value": {"uk": "5 м", "ru": "5 м"}, "is_main": True},
            {"key": {"uk": "Макс. вага собаки", "ru": "Макс. вес собаки"}, "value": {"uk": "20 кг", "ru": "20 кг"}, "is_main": True},
        ],
    },
    {
        "slug": "8in1-excel-vitamins-adult",
        "name": {"uk": "8in1 Excel мультивітаміни", "ru": "8in1 Excel мультивитамины"},
        "brand": "8in1",
        "description": {
            "uk": "Мультивітамінна добавка для дорослих собак. Містить вітаміни групи B, антиоксиданти та мінерали.",
            "ru": "Мультивитаминная добавка для взрослых собак. Содержит витамины группы B, антиоксиданты и минералы.",
        },
        "animals": ["dogs"],
        "categories": ["health", "vitamins"],
        "attributes": [
            {"key": {"uk": "Кількість", "ru": "Количество"}, "value": {"uk": "70 таблеток", "ru": "70 таблеток"}, "is_main": True},
            {"key": {"uk": "Вік", "ru": "Возраст"}, "value": {"uk": "Дорослі", "ru": "Взрослые"}, "is_main": True},
        ],
    },
    {
        "slug": "furminator-deshedding-cat",
        "name": {"uk": "FURminator дешеддер для котів", "ru": "FURminator дешеддер для кошек"},
        "brand": "FURminator",
        "description": {
            "uk": "Інструмент для видалення підшерстя у короткошерстих котів. Зменшує линяння до 90%.",
            "ru": "Инструмент для удаления подшёрстка у короткошёрстных кошек. Снижает линьку до 90%.",
        },
        "animals": ["cats"],
        "categories": ["health", "grooming"],
        "attributes": [
            {"key": {"uk": "Тип шерсті", "ru": "Тип шерсти"}, "value": {"uk": "Коротка", "ru": "Короткая"}, "is_main": True},
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "S", "ru": "S"}, "is_main": True},
        ],
    },
    {
        "slug": "trixie-cat-bed-minou",
        "name": {"uk": "Trixie Minou лежанка", "ru": "Trixie Minou лежанка"},
        "brand": "Trixie",
        "description": {
            "uk": "М'яка плюшева лежанка для котів та маленьких собак. Бортики та подушка для максимального комфорту.",
            "ru": "Мягкая плюшевая лежанка для кошек и маленьких собак. Бортики и подушка для максимального комфорта.",
        },
        "animals": ["cats", "dogs"],
        "categories": ["housing", "beds"],
        "attributes": [
            {"key": {"uk": "Розмір", "ru": "Размер"}, "value": {"uk": "50×40 см", "ru": "50×40 см"}, "is_main": True},
            {"key": {"uk": "Матеріал", "ru": "Материал"}, "value": {"uk": "Плюш", "ru": "Плюш"}, "is_main": True},
            {"key": {"uk": "Колір", "ru": "Цвет"}, "value": {"uk": "Бежевий", "ru": "Бежевый"}, "is_main": False},
        ],
    },
]


def seed_products(db: Session) -> None:
    from app.models.product import ProductAttribute

    for data in PRODUCTS:
        existing = db.query(Product).filter(Product.slug == data["slug"]).first()
        if existing:
            existing.name = data["name"]
            existing.description = data["description"]
            for old_attr in existing.attributes:
                db.delete(old_attr)
            db.flush()
            for attr in data.get("attributes", []):
                db.add(ProductAttribute(
                    id=uuid.uuid4(),
                    product_id=existing.id,
                    key=attr["key"],
                    value=attr["value"],
                    is_main=attr.get("is_main", False),
                ))
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
