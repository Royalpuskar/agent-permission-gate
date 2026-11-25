"""Sequential multi-agent execution with registered gateways and dependency failure propagation."""
from audit import Audit

def execute(plan, gateways, *, approvals=frozenset()):
    audit = Audit()
    states = {}
    # Validate the complete ordered graph before any effects.
    known = set()
    for step in plan:
        key = step["id"]
        if not isinstance(key, str) or not key or key in known:
            raise ValueError("invalid step id")
        deps = step.get("depends_on", [])
        if not isinstance(deps, list) or any(d not in known for d in deps):
            raise ValueError("invalid dependencies")
        known.add(key)
    for step in plan:
        key = step["id"]
        if any(states[d] != "completed" for d in step.get("depends_on", [])):
            status = "dependency-blocked"
        else:
            try:
                gateways[step["agent"]].dispatch(step["tool"], step.get("arguments", {}),
                                                approved=key in approvals)
                status = "completed"
            except Exception:
                # No automatic retry: a failed handler may already have side effects.
                status = "failed"
        states[key] = status
        audit.append(key, status)
    return states, audit.entries
