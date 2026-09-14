from plotly import graph_objects as go
VRA_BLUE, VRA_SKY, VRA_RED = "#0d4e95", "#94bde5", "#c0281a"
def sales_line(rows):
    return go.Figure(go.Scatter(x=[r["dia"] for r in rows], y=[float(r["venda_liquida"] or 0) for r in rows], mode="lines+markers", line={"color": VRA_BLUE, "width": 3}, name="Venda líquida")).update_layout(template="plotly_white", margin={"l": 20,"r": 12,"t": 32,"b": 20}, title="Evolução da venda líquida", paper_bgcolor="white")
def sales_combo(rows):
    return go.Figure(go.Bar(x=[r["dia"] for r in rows], y=[float(r["venda_liquida"] or 0) for r in rows], marker_color=VRA_SKY, name="Venda líquida")).update_layout(template="plotly_white", margin={"l":20,"r":12,"t":32,"b":20}, title="Venda diária", paper_bgcolor="white")
