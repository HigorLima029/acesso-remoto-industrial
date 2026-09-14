from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações centrais da aplicação.
    Valores lidos do arquivo .env (ver .env.example).
    """

    database_url: str = "postgresql://acesso_remoto:acesso_remoto@localhost:5432/acesso_remoto_industrial"

    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    wg_server_endpoint: str = ""
    wg_server_public_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
