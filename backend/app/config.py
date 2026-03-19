from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://fashionanimals:changeme@postgres:5432/fashionanimals"

    # JWT
    JWT_SECRET_KEY: str = "changeme_generate_random_secret_at_least_32_chars"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # App
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:80"

    # Admin seed
    ADMIN_EMAIL: str = "admin@fashionanimals"
    ADMIN_PASSWORD: str = "changeme_admin_password"

    # Upload
    UPLOAD_DIR: str = "/app/uploaded_media"
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5MB
    MAX_IMAGES_PER_PRODUCT: int = 10

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
