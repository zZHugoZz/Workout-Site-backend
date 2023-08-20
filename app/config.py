from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str

    secret_key: str
    refresh_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    spoonacular_api_key: str


settings = Settings()
