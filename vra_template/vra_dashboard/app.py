from dash import Dash
from redis import Redis
from .config import Settings
from .cache import RedisQueryCache
from .dashboards.analise_venda_mk.page import build_layout, register_callbacks
from .dashboards.analise_venda_mk.repository import SalesRepository
def create_app(settings: Settings | None = None) -> Dash:
    settings = settings or Settings.from_env()
    app = Dash(__name__, title="VRA | Análise de Venda", assets_folder="assets", suppress_callback_exceptions=True)
    app.layout = build_layout()
    repository = SalesRepository(settings.dw_dsn) if settings.dw_dsn else None
    cache = RedisQueryCache(Redis.from_url(settings.redis_url, decode_responses=True), settings.cache_ttl_seconds, settings.dw_refresh_marker)
    register_callbacks(app, repository, cache)
    return app
