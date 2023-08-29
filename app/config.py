from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # env_file = ".env" # Use with alembic
        env_file = "./.env" # Use with uvicorn

settings = Settings()

