"""Seed script: populates the database with catalog data."""

import uuid

import bcrypt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401,F403
from app.models.admin_user import AdminUser
from app.models.animal import Animal
from app.models.category import Category
from app.models.product import Product, ProductAttribute, ProductImage


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


ANIMALS = [
    {"slug": "dogs", "name": {"uk": "Собаки", "ru": "Собаки"}},
    {"slug": "cats", "name": {"uk": "Коти", "ru": "Кошки"}},
]

CATEGORIES = [
    {
        "slug": "feeders",
        "name": {"uk": "Підставки для мисок", "ru": "Подставки для мисок"},
        "children": [
            {"slug": "feeders-s", "name": {"uk": "Розмір S (24×13 см)", "ru": "Размер S (24×13 см)"}},
            {"slug": "feeders-m", "name": {"uk": "Розмір M (29×15 см)", "ru": "Размер M (29×15 см)"}},
            {"slug": "feeders-l", "name": {"uk": "Розмір L (36×20 см)", "ru": "Размер L (36×20 см)"}},
        ],
    },
    {
        "slug": "hammock-tables",
        "name": {"uk": "Журнальні столи-гамаки", "ru": "Журнальные столы-гамаки"},
        "children": [],
    },
    {
        "slug": "pet-beds",
        "name": {"uk": "Ліжечка для тварин", "ru": "Лежанки для животных"},
        "children": [],
    },
]


def feeder_attrs(size_uk, size_ru, height, bowl_volume, bowl_diameter, frame_color_uk, frame_color_ru, price):
    return [
        {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": f"{price} ₴", "ru": f"{price} ₴"}, "is_main": True},
        {"key": {"uk": "Розміри", "ru": "Размеры"}, "value": {"uk": size_uk, "ru": size_ru}, "is_main": True},
        {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": f"{height} см", "ru": f"{height} см"}, "is_main": False},
        {"key": {"uk": "Об'єм мисок", "ru": "Объём мисок"}, "value": {"uk": f"2 × {bowl_volume} мл", "ru": f"2 × {bowl_volume} мл"}, "is_main": False},
        {"key": {"uk": "Діаметр мисок", "ru": "Диаметр мисок"}, "value": {"uk": f"{bowl_diameter} см", "ru": f"{bowl_diameter} см"}, "is_main": False},
        {"key": {"uk": "Колір каркасу", "ru": "Цвет каркаса"}, "value": {"uk": frame_color_uk, "ru": frame_color_ru}, "is_main": True},
        {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Сталь з порошковим фарбуванням", "ru": "Сталь с порошковым покрытием"}, "is_main": False},
        {"key": {"uk": "Матеріал ніжок", "ru": "Материал ножек"}, "value": {"uk": "Силікон", "ru": "Силикон"}, "is_main": False},
        {"key": {"uk": "Матеріал мисок", "ru": "Материал мисок"}, "value": {"uk": "Харчова нержавіюча сталь", "ru": "Пищевая нержавеющая сталь"}, "is_main": False},
        {"key": {"uk": "Миски", "ru": "Миски"}, "value": {"uk": "TM Trixie (Німеччина)", "ru": "TM Trixie (Германия)"}, "is_main": False},
    ]


FEEDER_DESCRIPTION = {
    "uk": (
        "Підставка для мисок у стилі лофт. Каркас виготовлений зі сталі, "
        "силіконові ніжки не ковзають та не пошкоджують підлогу. "
        "Миски TM Trixie з харчової нержавіючої сталі європейської якості. "
        "Ніжки вставлені в отвори — не відпадають під час використання."
    ),
    "ru": (
        "Подставка для мисок в стиле лофт. Каркас изготовлен из стали, "
        "силиконовые ножки не скользят и не повреждают пол. "
        "Миски TM Trixie из пищевой нержавеющей стали европейского качества. "
        "Ножки вставлены в отверстия — не выпадают во время использования."
    ),
}

PRODUCTS = [
    # ── Підставки S (24×13 см) ───────────────────────────────────────────────
    {
        "slug": "feeder-s-black",
        "name": {"uk": "Підставка для мисок 24×13 см — Чорна", "ru": "Подставка для мисок 24×13 см — Чёрная"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-s"],
        "images": [
            {"url": "/images/Кормушка чёрная.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка чёрная с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка чёрная вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("24×13 см", "24×13 см", 5, 200, 10, "Чорний", "Чёрный", 900),
    },
    {
        "slug": "feeder-s-gray",
        "name": {"uk": "Підставка для мисок 24×13 см — Сіра (Графіт)", "ru": "Подставка для мисок 24×13 см — Серая (Графит)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-s"],
        "images": [
            {"url": "/images/Кормушка серая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка серая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка серая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("24×13 см", "24×13 см", 5, 200, 10, "Сірий (графіт)", "Серый (графит)", 900),
    },
    {
        "slug": "feeder-s-white",
        "name": {"uk": "Підставка для мисок 24×13 см — Біла", "ru": "Подставка для мисок 24×13 см — Белая"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-s"],
        "images": [
            {"url": "/images/Кормушка белая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка белая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка белая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("24×13 см", "24×13 см", 5, 200, 10, "Білий", "Белый", 900),
    },
    {
        "slug": "feeder-s-stainless",
        "name": {"uk": "Підставка для мисок 24×13 см — Нержавіюча сталь (глянець)", "ru": "Подставка для мисок 24×13 см — Нержавеющая сталь (глянец)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-s"],
        "images": [
            {"url": "/images/Кормушка нержавейка.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка нержавейка с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка нержавейка вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("24×13 см", "24×13 см", 5, 200, 10, "Нержавіюча сталь (глянець)", "Нержавеющая сталь (глянец)", 900),
    },

    # ── Підставки M (29×15 см) ───────────────────────────────────────────────
    {
        "slug": "feeder-m-black",
        "name": {"uk": "Підставка для мисок 29×15 см — Чорна", "ru": "Подставка для мисок 29×15 см — Чёрная"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-m"],
        "images": [
            {"url": "/images/Кормушка чёрная.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка чёрная с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка чёрная вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("29×15 см", "29×15 см", 7, 450, 13, "Чорний", "Чёрный", 1000),
    },
    {
        "slug": "feeder-m-gray",
        "name": {"uk": "Підставка для мисок 29×15 см — Сіра (Графіт)", "ru": "Подставка для мисок 29×15 см — Серая (Графит)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-m"],
        "images": [
            {"url": "/images/Кормушка серая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка серая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка серая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("29×15 см", "29×15 см", 7, 450, 13, "Сірий (графіт)", "Серый (графит)", 1000),
    },
    {
        "slug": "feeder-m-white",
        "name": {"uk": "Підставка для мисок 29×15 см — Біла", "ru": "Подставка для мисок 29×15 см — Белая"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-m"],
        "images": [
            {"url": "/images/Кормушка белая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка белая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка белая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("29×15 см", "29×15 см", 7, 450, 13, "Білий", "Белый", 1000),
    },
    {
        "slug": "feeder-m-stainless",
        "name": {"uk": "Підставка для мисок 29×15 см — Нержавіюча сталь (глянець)", "ru": "Подставка для мисок 29×15 см — Нержавеющая сталь (глянец)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-m"],
        "images": [
            {"url": "/images/Кормушка нержавейка.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка нержавейка с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка нержавейка вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("29×15 см", "29×15 см", 7, 450, 13, "Нержавіюча сталь (глянець)", "Нержавеющая сталь (глянец)", 1200),
    },

    # ── Підставки L (36×20 см) ───────────────────────────────────────────────
    {
        "slug": "feeder-l-black",
        "name": {"uk": "Підставка для мисок 36×20 см — Чорна", "ru": "Подставка для мисок 36×20 см — Чёрная"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-l"],
        "images": [
            {"url": "/images/Кормушка чёрная.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка чёрная с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка чёрная вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("36×20 см", "36×20 см", 15, 750, 17, "Чорний", "Чёрный", 1200),
    },
    {
        "slug": "feeder-l-gray",
        "name": {"uk": "Підставка для мисок 36×20 см — Сіра (Графіт)", "ru": "Подставка для мисок 36×20 см — Серая (Графит)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-l"],
        "images": [
            {"url": "/images/Кормушка серая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка серая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка серая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("36×20 см", "36×20 см", 15, 750, 17, "Сірий (графіт)", "Серый (графит)", 1200),
    },
    {
        "slug": "feeder-l-white",
        "name": {"uk": "Підставка для мисок 36×20 см — Біла", "ru": "Подставка для мисок 36×20 см — Белая"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-l"],
        "images": [
            {"url": "/images/Кормушка белая.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка белая с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка белая вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("36×20 см", "36×20 см", 15, 750, 17, "Білий", "Белый", 1200),
    },
    {
        "slug": "feeder-l-stainless",
        "name": {"uk": "Підставка для мисок 36×20 см — Нержавіюча сталь (глянець)", "ru": "Подставка для мисок 36×20 см — Нержавеющая сталь (глянец)"},
        "brand": "FashionAnimals",
        "description": FEEDER_DESCRIPTION,
        "animals": ["cats", "dogs"],
        "categories": ["feeders", "feeders-l"],
        "images": [
            {"url": "/images/Кормушка нержавейка.jpg", "order": 0, "is_main": True},
            {"url": "/images/кормушка нержавейка с котом.jpg", "order": 1, "is_main": False},
            {"url": "/images/кормушка нержавейка вид сверху.jpg", "order": 2, "is_main": False},
        ],
        "attributes": feeder_attrs("36×20 см", "36×20 см", 15, 750, 17, "Нержавіюча сталь (глянець)", "Нержавеющая сталь (глянец)", 1500),
    },

    # ── Журнальні столи-гамаки ────────────────────────────────────────────────
    {
        "slug": "table-round-gray",
        "name": {"uk": "Журнальний стіл-гамак круглий — Бетон-стайл", "ru": "Журнальный стол-гамак круглый — Бетон-стайл"},
        "brand": "FashionAnimals",
        "description": {
            "uk": (
                "Журнальний стіл-гамак 2в1 — для вас і вашого улюбленця. "
                "Тепер можна релаксувати, насолоджуватись кавою чи працювати за ноутбуком "
                "і одночасно пестити свого пухнастика, який також може відпочивати поруч. "
                "Каркас зі сталі з порошковим фарбуванням, стільниця з МДФ, гамак — тканина антикіготь. "
                "Легко збирається/розбирається. Ключ у комплекті. У розібраному вигляді 50×50×7 см."
            ),
            "ru": (
                "Журнальный стол-гамак 2в1 — для вас и вашего питомца. "
                "Теперь можно расслабляться, наслаждаться кофе или работать за ноутбуком "
                "и одновременно гладить своего питомца, который тоже может отдыхать рядом. "
                "Каркас из стали с порошковым покрытием, столешница из МДФ, гамак — ткань антикоготь. "
                "Легко собирается/разбирается. Ключ в комплекте. В разобранном виде 50×50×7 см."
            ),
        },
        "animals": ["cats", "dogs"],
        "categories": ["hammock-tables"],
        "images": [
            {"url": "/images/столик круг без кота.jpg", "order": 0, "is_main": True},
            {"url": "/images/стол круг + кот жёлтый фон.jpg", "order": 1, "is_main": False},
            {"url": "/images/стол круг собака.jpg", "order": 2, "is_main": False},
        ],
        "attributes": [
            {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": "2500 ₴", "ru": "2500 ₴"}, "is_main": True},
            {"key": {"uk": "Форма", "ru": "Форма"}, "value": {"uk": "Кругла", "ru": "Круглая"}, "is_main": True},
            {"key": {"uk": "Діаметр", "ru": "Диаметр"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Колір стільниці", "ru": "Цвет столешницы"}, "value": {"uk": "Бетон-стайл", "ru": "Бетон-стайл"}, "is_main": True},
            {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Сталь з порошковим фарбуванням", "ru": "Сталь с порошковым покрытием"}, "is_main": False},
            {"key": {"uk": "Матеріал стільниці", "ru": "Материал столешницы"}, "value": {"uk": "МДФ", "ru": "МДФ"}, "is_main": False},
            {"key": {"uk": "Матеріал гамака", "ru": "Материал гамака"}, "value": {"uk": "Тканина антикіготь", "ru": "Ткань антикоготь"}, "is_main": False},
        ],
    },
    {
        "slug": "table-round-wood",
        "name": {"uk": "Журнальний стіл-гамак круглий — Натуральне дерево", "ru": "Журнальный стол-гамак круглый — Натуральное дерево"},
        "brand": "FashionAnimals",
        "description": {
            "uk": (
                "Журнальний стіл-гамак 2в1 — для вас і вашого улюбленця. "
                "Стільниця з натурального дерева, покрита маслом-воском. "
                "Каркас зі сталі з порошковим фарбуванням, гамак — тканина антикіготь. "
                "Легко збирається/розбирається. Ключ у комплекті. У розібраному вигляді 50×50×7 см."
            ),
            "ru": (
                "Журнальный стол-гамак 2в1 — для вас и вашего питомца. "
                "Столешница из натурального дерева, покрыта маслом-воском. "
                "Каркас из стали с порошковым покрытием, гамак — ткань антикоготь. "
                "Легко собирается/разбирается. Ключ в комплекте. В разобранном виде 50×50×7 см."
            ),
        },
        "animals": ["cats", "dogs"],
        "categories": ["hammock-tables"],
        "images": [
            {"url": "/images/стол круг с домовёнком.jpg", "order": 0, "is_main": True},
            {"url": "/images/стол круг ноут + кот.jpg", "order": 1, "is_main": False},
            {"url": "/images/стол круг.jpg", "order": 2, "is_main": False},
        ],
        "attributes": [
            {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": "2500 ₴", "ru": "2500 ₴"}, "is_main": True},
            {"key": {"uk": "Форма", "ru": "Форма"}, "value": {"uk": "Кругла", "ru": "Круглая"}, "is_main": True},
            {"key": {"uk": "Діаметр", "ru": "Диаметр"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Колір стільниці", "ru": "Цвет столешницы"}, "value": {"uk": "Натуральне дерево", "ru": "Натуральное дерево"}, "is_main": True},
            {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Сталь з порошковим фарбуванням", "ru": "Сталь с порошковым покрытием"}, "is_main": False},
            {"key": {"uk": "Матеріал стільниці", "ru": "Материал столешницы"}, "value": {"uk": "Натуральне дерево (покрите маслом-воском)", "ru": "Натуральное дерево (покрыто маслом-воском)"}, "is_main": False},
            {"key": {"uk": "Матеріал гамака", "ru": "Материал гамака"}, "value": {"uk": "Тканина антикіготь", "ru": "Ткань антикоготь"}, "is_main": False},
        ],
    },
    {
        "slug": "table-square-gray",
        "name": {"uk": "Журнальний стіл-гамак квадратний — Бетон-стайл", "ru": "Журнальный стол-гамак квадратный — Бетон-стайл"},
        "brand": "FashionAnimals",
        "description": {
            "uk": (
                "Журнальний стіл-гамак 2в1 квадратної форми — для вас і вашого улюбленця. "
                "Стільниця МДФ у кольорі бетон-стайл. "
                "Каркас зі сталі з порошковим фарбуванням, гамак — тканина антикіготь. "
                "Легко збирається/розбирається. Ключ у комплекті. У розібраному вигляді 50×50×7 см."
            ),
            "ru": (
                "Журнальный стол-гамак 2в1 квадратной формы — для вас и вашего питомца. "
                "Столешница МДФ в цвете бетон-стайл. "
                "Каркас из стали с порошковым покрытием, гамак — ткань антикоготь. "
                "Легко собирается/разбирается. Ключ в комплекте. В разобранном виде 50×50×7 см."
            ),
        },
        "animals": ["cats", "dogs"],
        "categories": ["hammock-tables"],
        "images": [
            {"url": "/images/столик квадрат с котом.jpg", "order": 0, "is_main": True},
            {"url": "/images/Стол квадр кот.jpg", "order": 1, "is_main": False},
            {"url": "/images/стол квадр собака.jpg", "order": 2, "is_main": False},
        ],
        "attributes": [
            {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": "2500 ₴", "ru": "2500 ₴"}, "is_main": True},
            {"key": {"uk": "Форма", "ru": "Форма"}, "value": {"uk": "Квадратна", "ru": "Квадратная"}, "is_main": True},
            {"key": {"uk": "Розміри стільниці", "ru": "Размеры столешницы"}, "value": {"uk": "50×50 см", "ru": "50×50 см"}, "is_main": False},
            {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Колір стільниці", "ru": "Цвет столешницы"}, "value": {"uk": "Бетон-стайл", "ru": "Бетон-стайл"}, "is_main": True},
            {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Сталь з порошковим фарбуванням", "ru": "Сталь с порошковым покрытием"}, "is_main": False},
            {"key": {"uk": "Матеріал стільниці", "ru": "Материал столешницы"}, "value": {"uk": "МДФ", "ru": "МДФ"}, "is_main": False},
            {"key": {"uk": "Матеріал гамака", "ru": "Материал гамака"}, "value": {"uk": "Тканина антикіготь", "ru": "Ткань антикоготь"}, "is_main": False},
        ],
    },
    {
        "slug": "table-square-wood",
        "name": {"uk": "Журнальний стіл-гамак квадратний — Натуральне дерево", "ru": "Журнальный стол-гамак квадратный — Натуральное дерево"},
        "brand": "FashionAnimals",
        "description": {
            "uk": (
                "Журнальний стіл-гамак 2в1 квадратної форми — для вас і вашого улюбленця. "
                "Стільниця з натурального дерева, покрита маслом-воском. "
                "Каркас зі сталі з порошковим фарбуванням, гамак — тканина антикіготь. "
                "Легко збирається/розбирається. Ключ у комплекті. У розібраному вигляді 50×50×7 см."
            ),
            "ru": (
                "Журнальный стол-гамак 2в1 квадратной формы — для вас и вашего питомца. "
                "Столешница из натурального дерева, покрыта маслом-воском. "
                "Каркас из стали с порошковым покрытием, гамак — ткань антикоготь. "
                "Легко собирается/разбирается. Ключ в комплекте. В разобранном виде 50×50×7 см."
            ),
        },
        "animals": ["cats", "dogs"],
        "categories": ["hammock-tables"],
        "images": [
            {"url": "/images/стол квадрат на коврике.jpg", "order": 0, "is_main": True},
            {"url": "/images/стол квадрат + кот + глобус.jpg", "order": 1, "is_main": False},
            {"url": "/images/стол квадрат + кот + ноут.jpg", "order": 2, "is_main": False},
        ],
        "attributes": [
            {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": "2500 ₴", "ru": "2500 ₴"}, "is_main": True},
            {"key": {"uk": "Форма", "ru": "Форма"}, "value": {"uk": "Квадратна", "ru": "Квадратная"}, "is_main": True},
            {"key": {"uk": "Розміри стільниці", "ru": "Размеры столешницы"}, "value": {"uk": "50×50 см", "ru": "50×50 см"}, "is_main": False},
            {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": "50 см", "ru": "50 см"}, "is_main": False},
            {"key": {"uk": "Колір стільниці", "ru": "Цвет столешницы"}, "value": {"uk": "Натуральне дерево", "ru": "Натуральное дерево"}, "is_main": True},
            {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Сталь з порошковим фарбуванням", "ru": "Сталь с порошковым покрытием"}, "is_main": False},
            {"key": {"uk": "Матеріал стільниці", "ru": "Материал столешницы"}, "value": {"uk": "Натуральне дерево (покрите маслом-воском)", "ru": "Натуральное дерево (покрыто маслом-воском)"}, "is_main": False},
            {"key": {"uk": "Матеріал гамака", "ru": "Материал гамака"}, "value": {"uk": "Тканина антикіготь", "ru": "Ткань антикоготь"}, "is_main": False},
        ],
    },

    # ── Ліжечко ───────────────────────────────────────────────────────────────
    {
        "slug": "pet-bed-wooden",
        "name": {"uk": "Ліжечко дерев'яне для котів та собак", "ru": "Кроватка деревянная для кошек и собак"},
        "brand": "FashionAnimals",
        "description": {
            "uk": (
                "Ліжечко призначене для котиків, собак малого та середнього розмірів. "
                "Каркас виготовлений з масиву натурального дерева, покритого маслом-воском — "
                "гіпоалергенний та антистатичний. "
                "Перина з тканини антикіготь, наповнювач — поролон 2 см + 2 шари синтепону, "
                "завдяки чому перина не просідає та має ортопедичний ефект. "
                "Знімний чохол перини — можна прати. "
                "Легко збирається/розбирається. Ключ у комплекті. У розібраному вигляді 60×40×9 см."
            ),
            "ru": (
                "Кроватка предназначена для кошек, собак малого и среднего размеров. "
                "Каркас изготовлен из массива натурального дерева, покрытого маслом-воском — "
                "гипоаллергенный и антистатический. "
                "Перина из ткани антикоготь, наполнитель — поролон 2 см + 2 слоя синтепона, "
                "благодаря чему перина не проседает и имеет ортопедический эффект. "
                "Съёмный чехол перины — можно стирать. "
                "Легко собирается/разбирается. Ключ в комплекте. В разобранном виде 60×40×9 см."
            ),
        },
        "animals": ["cats", "dogs"],
        "categories": ["pet-beds"],
        "images": [
            {"url": "/images/кроватка без ничего.jpg", "order": 0, "is_main": True},
            {"url": "/images/кроватка с подушкой.jpg", "order": 1, "is_main": False},
            {"url": "/images/кровать кот.jpg", "order": 2, "is_main": False},
        ],
        "attributes": [
            {"key": {"uk": "Ціна", "ru": "Цена"}, "value": {"uk": "2400 ₴", "ru": "2400 ₴"}, "is_main": True},
            {"key": {"uk": "Розміри", "ru": "Размеры"}, "value": {"uk": "60×40 см", "ru": "60×40 см"}, "is_main": True},
            {"key": {"uk": "Висота", "ru": "Высота"}, "value": {"uk": "40 см", "ru": "40 см"}, "is_main": False},
            {"key": {"uk": "Матеріал каркасу", "ru": "Материал каркаса"}, "value": {"uk": "Масив натурального дерева (покрито маслом-воском)", "ru": "Массив натурального дерева (покрыто маслом-воском)"}, "is_main": False},
            {"key": {"uk": "Матеріал перини", "ru": "Материал перины"}, "value": {"uk": "Тканина антикіготь", "ru": "Ткань антикоготь"}, "is_main": False},
            {"key": {"uk": "Наповнювач", "ru": "Наполнитель"}, "value": {"uk": "Поролон 2 см + синтепон 2 шари", "ru": "Поролон 2 см + синтепон 2 слоя"}, "is_main": False},
            {"key": {"uk": "Особливості", "ru": "Особенности"}, "value": {"uk": "Гіпоалергенний, антистатичний, знімний чохол, ортопедичний ефект", "ru": "Гипоаллергенный, антистатический, съёмный чехол, ортопедический эффект"}, "is_main": False},
        ],
    },
]


# ── Seeding functions ──────────────────────────────────────────────────────────

def clear_data(db: Session) -> None:
    from sqlalchemy import text
    db.execute(text("DELETE FROM product_animals"))
    db.execute(text("DELETE FROM product_categories"))
    db.execute(text("DELETE FROM product_images"))
    db.execute(text("DELETE FROM product_attributes"))
    db.execute(text("DELETE FROM products"))
    db.execute(text("DELETE FROM categories"))
    db.execute(text("DELETE FROM animals"))
    db.commit()
    print("  Cleared existing data.")


def seed_animals(db: Session) -> None:
    for data in ANIMALS:
        db.add(Animal(id=uuid.uuid4(), **data))
    db.commit()
    print(f"  Animals: {db.query(Animal).count()} records")


def seed_categories(db: Session) -> None:
    for cat_data in CATEGORIES:
        parent = Category(
            id=uuid.uuid4(),
            slug=cat_data["slug"],
            name=cat_data["name"],
            parent_id=None,
        )
        db.add(parent)
        db.flush()
        for child_data in cat_data.get("children", []):
            db.add(Category(
                id=uuid.uuid4(),
                slug=child_data["slug"],
                name=child_data["name"],
                parent_id=parent.id,
            ))
    db.commit()
    print(f"  Categories: {db.query(Category).count()} records")


def seed_admin(db: Session) -> None:
    existing = db.query(AdminUser).filter(AdminUser.email == settings.ADMIN_EMAIL).first()
    if not existing:
        db.add(AdminUser(
            id=uuid.uuid4(),
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
        ))
        db.commit()
        print(f"  Admin user created: {settings.ADMIN_EMAIL}")
    else:
        print(f"  Admin user already exists: {settings.ADMIN_EMAIL}")


def seed_products(db: Session) -> None:
    for data in PRODUCTS:
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
            product.animals = db.query(Animal).filter(Animal.slug.in_(animal_slugs)).all()

        category_slugs = data.get("categories", [])
        if category_slugs:
            product.categories = db.query(Category).filter(Category.slug.in_(category_slugs)).all()

        db.add(product)
        db.flush()

        for img in data.get("images", []):
            db.add(ProductImage(
                id=uuid.uuid4(),
                product_id=product.id,
                url=img["url"],
                order=img["order"],
                is_main=img["is_main"],
                media_type="image",
            ))

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
        clear_data(db)
        seed_animals(db)
        seed_categories(db)
        seed_admin(db)
        seed_products(db)
        print("Seeding complete!")
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
