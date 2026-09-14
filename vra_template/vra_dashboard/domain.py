from dataclasses import asdict, dataclass
from datetime import date
from typing import Any

@dataclass(frozen=True)
class DashboardFilters:
    start_date: date
    end_date: date
    units: tuple[str, ...] = ()
    departments: tuple[str, ...] = ()
    sectors: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()
    comparison: str = "ano_anterior"
    def normalized(self) -> dict[str, Any]:
        return {key: list(value) if isinstance(value, tuple) else value.isoformat() if isinstance(value, date) else value for key, value in asdict(self).items()}

@dataclass(frozen=True)
class KpiDTO:
    name: str
    value: float
    comparison_value: float | None
    unit: str

@dataclass(frozen=True)
class SeriesDTO:
    x: tuple[str, ...]
    current: tuple[float, ...]
    comparison: tuple[float, ...]

@dataclass(frozen=True)
class TableDTO:
    columns: tuple[str, ...]
    rows: tuple[dict[str, Any], ...]
    page: int
    page_size: int
    total_rows: int
