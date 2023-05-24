from pydantic import BaseSettings


class Settings(BaseSettings):
    RPC_USER: str
    RPC_PASSWORD: str
    RPC_HOST: str
    RPC_PORT: int

    class Config:
        env_file = "./.env"


cfg = Settings()