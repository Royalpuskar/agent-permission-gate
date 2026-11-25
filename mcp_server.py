"""Optional MCP server exposing read-only workflow preflight.
Install the official Python MCP SDK separately: pip install mcp.
Only synthetic example data is exposed; arbitrary paths are not accepted.
"""
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from guard import Guard
from preflight import preflight

server = FastMCP("permission-gate")

@server.tool()
def inspect_example() -> dict:
    """Inspect the bundled synthetic workflow without executing any actions."""
    data = json.loads(Path(__file__).with_name("workflow_demo.json").read_text())
    return preflight(data["plan"], Guard(data["subject"], data["grants"], clock=lambda: data["now"]), data["budget"])

if __name__ == "__main__":
    server.run(transport="stdio")
