from datetime import date
from vra_dashboard.cache import RedisQueryCache
from vra_dashboard.domain import DashboardFilters
class FakeRedis:
    def __init__(self): self.values = {}; self.ttl = None
    def get(self, key): return self.values.get(key)
    def setex(self, key, ttl, value): self.values[key] = value; self.ttl = ttl
def test_cache_reuses_versioned_result():
    redis = FakeRedis(); cache = RedisQueryCache(redis, 60, "refresh-1")
    filters = DashboardFilters(date(2026,1,1), date(2026,1,2))
    assert cache.get_or_load("q-v1", filters, lambda: {"value": 1}) == {"value": 1}
    assert cache.get_or_load("q-v1", filters, lambda: {"value": 2}) == {"value": 1}
    assert redis.ttl == 60 and cache.key("q-v1", filters) != cache.key("q-v2", filters)
