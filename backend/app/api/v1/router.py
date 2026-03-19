from fastapi import APIRouter

from app.api.v1.admin.routes import router as admin_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.public.animals import router as animals_router
from app.api.v1.public.categories import router as categories_router
from app.api.v1.public.products import router as products_router
from app.api.v1.public.search import router as search_router

api_router = APIRouter()

# Public endpoints
api_router.include_router(animals_router, prefix="/animals", tags=["animals"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(search_router, prefix="/search", tags=["search"])

# Auth
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Admin
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
