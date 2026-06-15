"""Tool logic, kept free of the MCP SDK so it can be tested directly.

Each tool calls finvariant and returns a JSON-safe dict: the audit report
(verdict, failing checks with expected vs actual, counts, provenance) plus a
plain-language summary.
"""

from __future__ import annotations

from finvariant import Statements, check
from finvariant.model import BS_SECTIONS, BS_TOTALS, CF_OTHER, CF_SECTIONS, IS_FIELDS

SIGN_CONVENTION = (
    "Income statement: revenue positive; expenses (cogs, operating_expenses, "
    "interest_expense, tax) as positive magnitudes. Balance sheet: lines positive "
    "as presented (treasury_stock and an accumulated deficit may be negative). "
    "Cash flow: every line signed by its effect on cash (inflows positive, "
    "outflows negative), so capex, debt_repaid, share_buybacks and dividends_paid "
    "are negative."
)

CHECKS = [
    "Footing: every subtotal equals the sum of its line items (all three statements).",
    "Accounting equation: total assets = total liabilities + total equity.",
    "Cash: net change = cfo + cfi + cff; ending cash ties to the balance sheet; "
    "beginning cash ties to the prior period.",
    "Articulation: net income agrees across statements; retained earnings = prior "
    "+ net income - dividends.",
]


def check_statements(periods, income_statement=None, balance_sheet=None,
                     cash_flow=None, abs_tol=0.5, rel_tol=1e-4) -> dict:
    """Verify a set of statements; return the audit report plus a summary."""
    try:
        statements = Statements(
            periods=periods,
            income_statement=income_statement or {},
            balance_sheet=balance_sheet or {},
            cash_flow=cash_flow or {},
        )
        report = check(statements, abs_tol=abs_tol, rel_tol=rel_tol)
    except (ValueError, TypeError) as exc:
        return {
            "error": str(exc),
            "hint": "call describe_schema for the valid fields and the sign convention",
        }
    result = report.to_dict()
    result["summary"] = report.summary()
    return result


def describe_schema() -> dict:
    """The canonical fields by statement, the sign convention and the checks."""
    return {
        "sign_convention": SIGN_CONVENTION,
        "income_statement_fields": sorted(IS_FIELDS),
        "balance_sheet": {
            "sections": {subtotal: list(items) for subtotal, items in BS_SECTIONS.items()},
            "totals": {total: list(parts) for total, parts in BS_TOTALS.items()},
        },
        "cash_flow": {
            "sections": {subtotal: list(items) for subtotal, items in CF_SECTIONS.items()},
            "other": list(CF_OTHER),
        },
        "checks": CHECKS,
        "notes": (
            "Provide only the fields you have; a check whose inputs are missing is "
            "skipped, not failed. To check that a subtotal foots, also provide its "
            "line items."
        ),
    }
