from pydantic import BaseSettings


class Settings(BaseSettings):
    NEO_PROFILE: str = "http://localhost:7474/"
    NEO_USER: str = "neo4j"
    NEO_PASSWORD: str = "Citrus130649"
    NEO_DB_NAME: str = "neo4j"


settings = Settings()
print(settings)
