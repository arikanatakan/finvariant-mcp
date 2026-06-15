import json

from finvariant_mcp import _tools


def _balanced(assets=100, liabilities=60, equity=40):
    return {"FY2024": {"total_assets": assets, "total_liabilities": liabilities,
                       "total_equity": equity}}


def test_check_passes():
    r = _tools.check_statements(periods=["FY2024"], balance_sheet=_balanced())
    assert r["ok"] is True
    assert r["counts"]["failed"] == 0
    assert "summary" in r and "finvariant" in r["summary"]


def test_check_fails_with_numbers():
    r = _tools.check_statements(periods=["FY2024"], balance_sheet=_balanced(assets=101))
    assert r["ok"] is False
    finding = next(f for f in r["findings"] if f["rule_id"] == "EQ.accounting_equation")
    assert finding["expected"] == 100 and finding["actual"] == 101


def test_unknown_field_returns_error_with_hint():
    r = _tools.check_statements(periods=["FY2024"],
                                balance_sheet={"FY2024": {"frobnicate": 1}})
    assert "error" in r
    assert "describe_schema" in r["hint"]


def test_result_is_json_serializable():
    r = _tools.check_statements(periods=["FY2024"], balance_sheet=_balanced())
    json.dumps(r)


def test_describe_schema():
    s = _tools.describe_schema()
    assert "revenue" in s["income_statement_fields"]
    assert "total_current_assets" in s["balance_sheet"]["sections"]
    assert "cfo" in s["cash_flow"]["sections"]
    assert s["sign_convention"]
    assert len(s["checks"]) >= 4
    json.dumps(s)
