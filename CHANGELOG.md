# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project uses
[semantic versioning](https://semver.org/).

## [0.1.0] - 2026-06-15

First release.

### Added

- `check_statements` tool: verifies income statement, balance sheet and cash
  flow data against the finvariant invariants (footing, the accounting equation,
  cash-flow tie-outs, articulation) and returns the audit report plus a
  plain-language summary.
- `describe_schema` tool: the canonical field names by statement, the sign
  convention and the invariants checked.
- stdio server built on FastMCP, with read-only tool annotations.
