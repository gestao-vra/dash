from vra_dashboard.formatters import currency_br, number_br, percent_br
def test_brazilian_formatting():
    assert currency_br(1234.5) == "R$ 1.234,50"
    assert number_br(1234.5, 1) == "1.234,5"
    assert percent_br(0.1234) == "12,3%"
