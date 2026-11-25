"""Local synchronous tool dispatcher; not an MCP server or sandbox."""
from dataclasses import dataclass
from typing import Callable
from guard import Guard, PermissionDenied


@dataclass(frozen=True)
class Tool:
    action: str
    resource: str
    handler: Callable


class ToolGateway:
    def __init__(self, guard: Guard, tools: dict[str, Tool]):
        self._guard = guard
        self._tools = dict(tools)

    def dispatch(self, name: str, arguments: dict, *, approved: bool = False):
        # Tool metadata and approval must come from trusted application code,
        # not from the agent's proposed arguments.
        if not isinstance(name, str) or name not in self._tools:
            raise PermissionDenied("unknown-tool")
        if not isinstance(arguments, dict) or not all(
            isinstance(key, str) for key in arguments
        ):
            raise PermissionDenied("invalid-arguments")
        tool = self._tools[name]
        decision = self._guard.check(tool.action, tool.resource, approved=approved)
        if decision.get("allowed") is not True:
            raise PermissionDenied(decision["reason"])
        return tool.handler(**arguments)
