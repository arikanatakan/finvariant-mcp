"""The MCP server: registers the finvariant tools and runs over stdio.

Both tools are pure, read-only computations, marked with annotations so a client
can present and auto-run them safely.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from . import _tools

mcp = FastMCP("finvariant")


def _annotations(title: str) -> ToolAnnotations:
    return ToolAnnotations(
        title=title,
        readOnlyHint=True,
        idempotentHint=True,
        openWorldHint=False,
    )


@mcp.tool(annotations=_annotations("Check financial statements"))
def check_statements(
    periods: list[str],
    income_statement: dict[str, dict[str, float]] | None = None,
    balance_sheet: dict[str, dict[str, float]] | None = None,
    cash_flow: dict[str, dict[str, float]] | None = None,
    abs_tol: float = 0.5,
    rel_tol: float = 1e-4,
) -> dict:
    """Verify a set of financial statements against the accounting invariants.

    Each statement maps a period label to a mapping of canonical field names to
    values; call describe_schema for the field names and the sign convention.
    Returns a verdict, the failing checks with expected vs actual, counts and a
    plain-language summary. Provide only the fields you have: a check whose
    inputs are missing is skipped, not failed.
    """
    return _tools.check_statements(
        periods, income_statement, balance_sheet, cash_flow, abs_tol, rel_tol
    )


@mcp.tool(annotations=_annotations("Describe the input schema"))
def describe_schema() -> dict:
    """The canonical field names by statement, the sign convention, and the
    invariants finvariant checks. Call this before check_statements to format
    the input correctly.
    """
    return _tools.describe_schema()


def main() -> None:
    """Console-script entry point: run the server on stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
