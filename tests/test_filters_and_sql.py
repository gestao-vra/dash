from datetime import date
from vra_dashboard.domain import DashboardFilters
from vra_dashboard.dashboards.analise_venda_mk.repository import SalesRepository
def test_normalized_filters_are_stable():
    filters = DashboardFilters(date(2026, 1, 1), date(2026, 1, 31), units=("001",))
    assert filters.normalized()["start_date"] == "2026-01-01"
    assert filters.normalized()["units"] == ["001"]
def test_sql_keeps_user_values_as_parameters():
    filters = DashboardFilters(date(2026, 1, 1), date(2026, 1, 31), units=("001' OR true --",))
    sql, params = SalesRepository("unused")._where(filters)
    assert "001' OR true" not in sql
    assert params[-1] == ["001' OR true --"]
    assert "%s" in sql
