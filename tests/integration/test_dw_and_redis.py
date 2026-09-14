import os
from datetime import date
import redis
from vra_dashboard.cache import RedisQueryCache
from vra_dashboard.domain import DashboardFilters
from vra_dashboard.dashboards.analise_venda_mk.repository import SalesRepository
def test_controlled_postgres_and_real_redis_return_cached_aggregate():
    filters = DashboardFilters(date(2026, 1, 1), date(2026, 1, 31), units=("001",))
    repository = SalesRepository(os.environ["DW_DSN"])
    client = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True); client.flushdb()
    cache = RedisQueryCache(client, 30, "fixture-1")
    first = cache.get_or_load(repository.query_version, filters, lambda: repository.snapshot(filters))
    second = cache.get_or_load(repository.query_version, filters, lambda: (_ for _ in ()).throw(AssertionError("DW should not be queried")))
    assert first == second and float(first["kpis"]["venda_liquida"]) == 100
