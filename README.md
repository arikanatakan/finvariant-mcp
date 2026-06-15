<!-- mcp-name: io.github.arikanatakan/finvariant-mcp -->

# finvariant-mcp

[![CI](https://github.com/arikanatakan/finvariant-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/arikanatakan/finvariant-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/finvariant-mcp?v=3)](https://pypi.org/project/finvariant-mcp/)
[![License: MIT](https://img.shields.io/github/license/arikanatakan/finvariant-mcp)](LICENSE)

An MCP server that exposes [finvariant](https://github.com/arikanatakan/finvariant),
the deterministic financial-statement integrity checker for Python, as a tool
for AI agents: hand it income statement, balance sheet and cash flow data and it
verifies that the balance sheet balances, the cash flow ties to the balance
sheet, subtotals foot, and the three statements articulate.

Agents asked to build, read or summarise financial statements tend to produce
the numbers themselves: a balance sheet that does not balance, a cash flow that
does not tie, a retained-earnings figure that does not roll forward. Generated
financial statements fail silently. The check belongs in a deterministic,
versioned, validated library that the agent calls; the agent chooses what to
verify and explains the verdict.

## Tools

| Tool | Purpose |
| ---- | ------- |
| `check_statements` | Verify statements against the accounting invariants; return a verdict, the failing checks with expected vs actual, counts, provenance and a plain-language summary. |
| `describe_schema` | The canonical field names by statement, the sign convention, and the invariants checked; call it first to format the input. |

Both tools are read-only and return finvariant's JSON-safe payload, so a client
can present and auto-run them safely.

## Installation

Run it with [uv](https://docs.astral.sh/uv/) (no install needed):

```
uvx finvariant-mcp
```

or install from PyPI:

```
pip install finvariant-mcp
```

## Configuration

Add it to your MCP client. For example:

```json
{
  "mcpServers": {
    "finvariant": {
      "command": "uvx",
      "args": ["finvariant-mcp"]
    }
  }
}
```

If you installed with pip, use `"command": "finvariant-mcp"` with no args.

## Example

An agent verifying a model it just built:

```
describe_schema()
  -> the field names, sign convention and the four invariant groups

check_statements(
  periods=["FY2024"],
  balance_sheet={"FY2024": {
    "total_assets": 540, "total_liabilities": 158, "total_equity": 380
  }},
)
  -> { "ok": false,
       "verdict": "FAIL - statements do not tie out",
       "findings": [ { "rule_id": "EQ.accounting_equation",
                       "expected": 538, "actual": 540, "difference": 2 } ],
       "summary": "finvariant audit - ...\n  Verdict: FAIL ..." }
```

## Design

The server is a thin, stateless wrapper. All accounting logic lives in the
finvariant library, which computes the invariants from their definitions and is
validated against the published statements of several real companies. The server
adds the tool schema, read-only annotations and an input-schema helper so an
agent can format the input and act on the result.

## Related

- [finvariant](https://github.com/arikanatakan/finvariant): the library this server wraps.

## License

MIT. Written and maintained by [Atakan Arikan](https://github.com/arikanatakan),
MSc Student at Tsinghua University and Politecnico di Milano.
