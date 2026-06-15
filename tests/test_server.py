def test_server_imports_and_wires_tools():
    from finvariant_mcp import server

    assert server.mcp is not None
    assert callable(server.main)


def test_tools_are_registered():
    import asyncio

    from finvariant_mcp import server

    tools = asyncio.run(server.mcp.list_tools())
    names = {t.name for t in tools}
    assert {"check_statements", "describe_schema"} <= names
