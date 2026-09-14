from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    dw_dsn: str
    redis_url: str
    app_port: int
    app_env: str
    cache_ttl_seconds: int
    dw_refresh_marker: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(os.environ.get("DW_DSN", ""), os.environ.get("REDIS_URL", "redis://localhost:6379/0"), int(os.environ.get("APP_PORT", "8050")), os.environ.get("APP_ENV", "development"), int(os.environ.get("CACHE_TTL_SECONDS", "300")), os.environ.get("DW_REFRESH_MARKER", "manual"))
