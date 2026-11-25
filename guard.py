"""Opt-in local permission guard for synchronous Python tools.

Not a sandbox: callers must route every protected action through this guard.
The caller is responsible for trusted identity, policy and approval inputs.
"""
from copy import deepcopy
from time import time
from engine import analyze


class PermissionDenied(RuntimeError):
    pass


class Guard:
    def __init__(self, subject, grants, clock=time):
        self.subject = subject
        self._grants = deepcopy(grants)
        self._clock = clock

    def check(self, action, resource, *, approved=False):
        try:
            if type(approved) is not bool:
                raise ValueError("approval must be boolean")
            return analyze({
                "now": self._clock(),
                "grants": self._grants,
                "request": {"subject": self.subject, "action": action,
                            "resource": resource, "approved": approved},
            })
        except (ValueError, TypeError, KeyError, OverflowError):
            return {"allowed": False, "reason": "invalid-policy"}

    def run(self, action, resource, tool, *args, approved=False, **kwargs):
        decision = self.check(action, resource, approved=approved)
        if decision.get("allowed") is not True:
            raise PermissionDenied(decision["reason"])
        return tool(*args, **kwargs)
