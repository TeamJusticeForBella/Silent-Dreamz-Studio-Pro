from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://bcc:bcc_password_change_me@localhost:5432/bcc"
    REDIS_URL: str = "redis://localhost:6379/0"
    NATS_URL: str = "nats://localhost:4222"
    OPENSEARCH_URL: str = "http://localhost:9200"
    QDRANT_URL: str = "http://localhost:6333"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "bccminio"
    MINIO_SECRET_KEY: str = "minio_password_change_me"
    MINIO_BUCKET_EVIDENCE: str = "evidence"
    MINIO_BUCKET_EXPORTS: str = "exports"
    MINIO_BUCKET_TRANSCRIPTS: str = "transcripts"
    MINIO_BUCKET_OCR: str = "ocr"
    MINIO_USE_SSL: bool = False
    TIKA_URL: str = "http://localhost:9998"
    GOTENBERG_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
