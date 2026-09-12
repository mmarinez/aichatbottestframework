import os
from dotenv import load_dotenv
from dataclasses import dataclass

class MissingConfig(Exception):
    """Raised when missing a required enviroment variable."""

@dataclass(frozen=True)
class Settings:
    base_url: str
    email: str
    password: str
    expect_timeout_ms: int

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            base_url=os.environ.get("APP_BASE_URL", "http://localhost:3000/"),
            email=cls._required("APP_USER_EMAIL"),
            password=cls._required("APP_USER_PASSWORD"),
            expect_timeout_ms=int(os.environ.get("EXPECT_TIMEOUT_MS", 10_000))
        )
    
    @staticmethod
    def _required(name: str) -> str:
        value = os.environ.get(name, "").strip()
        if not value:
            raise MissingConfig(
                f"{name} is not set. Copy .env.example to .env, "
                f"or export {name} before running pytest"
            )
        return value