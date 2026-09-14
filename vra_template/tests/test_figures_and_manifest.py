import json
from pathlib import Path
from vra_dashboard.dashboards.analise_venda_mk.figures import sales_line
def test_sales_figure_uses_vra_color():
    figure = sales_line([{"dia":"2026-01-01", "venda_liquida": 42}])
    assert figure.data[0].line.color == "#0d4e95"
def test_manifest_covers_all_pbip_visuals_at_desktop_canvas():
    path = Path(__file__).parents[1] / "vra_dashboard/dashboards/analise_venda_mk/manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["canvas"] == {"width": 1280, "height": 2000}
    assert len(manifest["visuals"]) == 36
    assert len({item["pbip"] for item in manifest["visuals"]}) == 36
