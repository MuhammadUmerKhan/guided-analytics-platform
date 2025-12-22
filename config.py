from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Retail Sales Analytics Platform"
    min_row_count: int = 50
    upload_dir: str = "uploads"

settings = Settings()