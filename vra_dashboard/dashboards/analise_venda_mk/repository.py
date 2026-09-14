"""Read-only, aggregated PostgreSQL access for the MK profile."""
from datetime import timedelta
from typing import Any
import psycopg
from psycopg.rows import dict_row
from ...domain import DashboardFilters
from ...telemetry import timed

SALE_FACT = "fat_venda_det_tipovenda"
CUSTOMER_FACT = "fat_qtde_clientes"

class SalesRepository:
    query_version = "analise-venda-mk-v1"
    def __init__(self, dsn: str) -> None: self.dsn = dsn

    def _where(self, filters: DashboardFilters, alias: str = "f") -> tuple[str, list[Any]]:
        clauses, params = [f"{alias}.data >= %s", f"{alias}.data < %s"], [filters.start_date, filters.end_date + timedelta(days=1)]
        for values, field in ((filters.units, f"{alias}.chv_unidade"), (filters.departments, "g.dsc_clas_departamento"), (filters.sectors, "g.dsc_clas_setor"), (filters.categories, "g.dsc_clas_categoria")):
            if values:
                clauses.append(f"{field} = ANY(%s)"); params.append(list(values))
        return " AND ".join(clauses), params

    def _rows(self, sql: str, params: list[Any]) -> list[dict[str, Any]]:
        with timed("dw_query", query_version=self.query_version):
            with psycopg.connect(self.dsn, row_factory=dict_row) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("BEGIN READ ONLY")
                    cursor.execute(sql, params)
                    return list(cursor.fetchall())

    def snapshot(self, filters: DashboardFilters, page: int = 0, page_size: int = 50) -> dict[str, Any]:
        """Return only page-facing aggregates; never a raw DW fact slice."""
        where, params = self._where(filters)
        base = f"""
          FROM dw.fat_principal f
          LEFT JOIN dw.dim_produto_unidade_total p ON p.chv_produto = f.chv_produto AND p.chv_unidade = f.chv_unidade
          LEFT JOIN dw.dim_grupo_produto_quebra_total g ON g.chv_produto = f.chv_produto
          WHERE {where}
        """
        kpis = self._rows(f"""SELECT
          COALESCE(SUM(f.valor_liq) FILTER (WHERE f.flg_tipo_fato = %s), 0) AS venda_liquida,
          COALESCE(SUM(f.lucro_liq) FILTER (WHERE f.flg_tipo_fato = %s), 0) AS lucro_liquido,
          COALESCE(SUM(f.qtde_cliente) FILTER (WHERE f.flg_tipo_fato = %s), 0) AS clientes,
          COALESCE(SUM(f.qtde_liq) FILTER (WHERE f.flg_tipo_fato = %s), 0) AS quantidade_liquida
          {base}""", [SALE_FACT, SALE_FACT, CUSTOMER_FACT, SALE_FACT, *params])[0]
        series = self._rows(f"""SELECT f.data::date AS dia, COALESCE(SUM(f.valor_liq), 0) AS venda_liquida
          {base} AND f.flg_tipo_fato = %s GROUP BY f.data::date ORDER BY dia""", [*params, SALE_FACT])
        offset, limit = max(page, 0) * min(max(page_size, 1), 100), min(max(page_size, 1), 100)
        detail = self._rows(f"""SELECT COALESCE(g.dsc_clas_departamento, 'Não classificado') AS departamento,
          COALESCE(g.dsc_clas_setor, 'Não classificado') AS setor, COALESCE(g.dsc_clas_categoria, 'Não classificado') AS categoria,
          SUM(f.valor_liq) AS venda_liquida, SUM(f.lucro_liq) AS lucro_liquido
          {base} AND f.flg_tipo_fato = %s GROUP BY 1,2,3 ORDER BY venda_liquida DESC LIMIT %s OFFSET %s""", [*params, SALE_FACT, limit, offset])
        return {"kpis": kpis, "series": series, "detail": detail, "page": page, "page_size": limit}
