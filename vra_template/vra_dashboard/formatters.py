from decimal import Decimal
def currency_br(value: float | Decimal | None) -> str:
    if value is None: return "—"
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def number_br(value: float | int | None, decimals: int = 0) -> str:
    if value is None: return "—"
    return f"{float(value):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def percent_br(value: float | None, decimals: int = 1) -> str:
    return "—" if value is None else f"{value * 100:.{decimals}f}".replace(".", ",") + "%"
