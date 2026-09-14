from datetime import date, timedelta
from dash import Dash, Input, Output, State, dcc, html, dash_table
from ...cache import RedisQueryCache
from ...domain import DashboardFilters
from ...formatters import currency_br, number_br, percent_br
from ...telemetry import timed
from .figures import sales_combo, sales_line
from .repository import SalesRepository

def build_layout():
    end, start = date.today(), date.today() - timedelta(days=30)
    dropdown = lambda ident, label: html.Div([html.Label(label), dcc.Dropdown(id=ident, multi=True, placeholder="Todos")], className="filter")
    return html.Main(className="vra-app", children=[
      html.Header([html.Img(src="/assets/logo-vra-branco.png", className="logo"), html.Div([html.Span("DASHBOARD", className="eyebrow"), html.H1("Análise de Venda – MK")])]),
      html.Section(className="filters", children=[dcc.DatePickerRange(id="period", start_date=start, end_date=end, display_format="DD/MM/YYYY"), dropdown("units", "Unidade"), dropdown("departments", "Departamento"), dropdown("sectors", "Setor"), dropdown("categories", "Categoria"), dcc.RadioItems(id="comparison", options=[{"label":"Ano anterior","value":"ano_anterior"},{"label":"Período","value":"periodo"}], value="ano_anterior", inline=True)]),
      dcc.Store(id="global-filter-state"), dcc.Store(id="visual-selection"), html.Div(id="safe-state", role="alert"), html.Div(id="kpi-row", className="kpi-row"),
      html.Section(className="chart-grid", children=[dcc.Loading(dcc.Graph(id="sales-line", config={"displayModeBar":False})), dcc.Loading(dcc.Graph(id="sales-combo", config={"displayModeBar":False}))]),
      html.P(id="selection-status", className="selection-status"), html.Section([html.H2("Venda por Departamento, Setor e Categoria"), dash_table.DataTable(id="detail-table", page_action="custom", page_current=0, page_size=50, sort_action="native", style_table={"overflowX":"auto"}, style_header={"backgroundColor":"#0d4e95", "color":"white", "fontWeight":"bold"})], className="table-card")])

def _filters(data):
    return DashboardFilters(date.fromisoformat(data["start_date"]), date.fromisoformat(data["end_date"]), tuple(data.get("units") or ()), tuple(data.get("departments") or ()), tuple(data.get("sectors") or ()), tuple(data.get("categories") or ()), data.get("comparison", "ano_anterior"))
def _card(label, value, sub=""):
    return html.Article([html.Span(label, className="kpi-label"), html.Strong(value), html.Small(sub)], className="kpi")
def _render(snapshot):
    k = snapshot["kpis"]; sales, profit, customers, quantity = (float(k[name] or 0) for name in ("venda_liquida","lucro_liquido","clientes","quantidade_liquida"))
    margin = profit / sales if sales else None; ticket = sales / customers if customers else None
    latest = snapshot["series"][-1]["dia"] if snapshot["series"] else "—"
    cards = [_card("Venda líquida", currency_br(sales)), _card("Meta de vendas", "—", "reconciliação pendente"), _card("Δ meta", "—", "reconciliação pendente"), _card("Lucro líquido", currency_br(profit)), _card("Margem", percent_br(margin)), _card("Clientes", number_br(customers)), _card("Ticket médio", currency_br(ticket)), _card("Quantidade líquida", number_br(quantity)), _card("Venda anterior", "—", "reconciliação pendente"), _card("Lucro anterior", "—", "reconciliação pendente"), _card("Atualizado", str(latest))]
    rows = [{**row, "venda_liquida": currency_br(row["venda_liquida"]), "lucro_liquido": currency_br(row["lucro_liquido"])} for row in snapshot["detail"]]
    columns = [{"name": name.replace("_", " ").title(), "id": name} for name in (rows[0].keys() if rows else ["departamento", "setor", "categoria", "venda_liquida", "lucro_liquido"])]
    return cards, sales_line(snapshot["series"]), sales_combo(snapshot["series"]), rows, columns

def register_callbacks(app: Dash, repository: SalesRepository | None, cache: RedisQueryCache):
    @app.callback(Output("global-filter-state", "data"), Input("period", "start_date"), Input("period", "end_date"), Input("units", "value"), Input("departments", "value"), Input("sectors", "value"), Input("categories", "value"), Input("comparison", "value"))
    def set_global_filters(start, end, units, departments, sectors, categories, comparison):
        return {"start_date": start, "end_date": end, "units": units or [], "departments": departments or [], "sectors": sectors or [], "categories": categories or [], "comparison": comparison}
    @app.callback(Output("visual-selection", "data"), Input("sales-line", "clickData"), prevent_initial_call=True)
    def select_visual(point): return point["points"][0].get("x") if point else None
    @app.callback(Output("selection-status", "children"), Input("visual-selection", "data"))
    def describe_selection(value): return f"Data selecionada: {value}" if value else "Selecione um ponto do gráfico para contextualizar a análise."
    @app.callback(Output("safe-state", "children"), Output("kpi-row", "children"), Output("sales-line", "figure"), Output("sales-combo", "figure"), Output("detail-table", "data"), Output("detail-table", "columns"), Input("global-filter-state", "data"), Input("detail-table", "page_current"), Input("detail-table", "page_size"))
    def refresh(filters_data, page, page_size):
        if repository is None: return "Configure DW_DSN para consultar o DW.", [], {}, {}, [], []
        try:
            filters = _filters(filters_data)
            with timed("page_render", dashboard="analise-venda-mk"):
                snapshot = cache.get_or_load(repository.query_version, filters, lambda: repository.snapshot(filters, page or 0, page_size or 50))
                cards, line, combo, rows, columns = _render(snapshot)
            return "", cards, line, combo, rows, columns
        except Exception:
            return "Não foi possível consultar dados verificados agora. Nenhum indicador parcial foi exibido.", [], {}, {}, [], []
