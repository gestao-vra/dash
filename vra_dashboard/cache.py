import hashlib
import json
from typing import Any, Callable
from .domain import DashboardFilters

class RedisQueryCache:
    def __init__(self, client: Any, ttl_seconds: int, refresh_marker: str) -> None:
        self.client, self.ttl_seconds, self.refresh_marker = client, ttl_seconds, refresh_marker
    def key(self, query_version: str, filters: DashboardFilters) -> str:
        material = {"query_version": query_version, "filters": filters.normalized(), "dw_refresh": self.refresh_marker}
        return "vra:dw:" + hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    def get_or_load(self, query_version: str, filters: DashboardFilters, load: Callable[[], Any]) -> Any:
        key = self.key(query_version, filters)
        cached = self.client.get(key)
        if cached is not None: return json.loads(cached)
        value = load()
        self.client.setex(key, self.ttl_seconds, json.dumps(value, default=str, separators=(",", ":")))
        return value
