"""Offline workflow preflight: inspect dependencies, policy and estimated cost.
No tools are executed. Costs are caller-supplied estimates, not measured usage.
"""
import argparse
import json
from decimal import Decimal, InvalidOperation
from guard import Guard

def preflight(plan, guard, budget):
    budget = Decimal(str(budget))
    if not budget.is_finite() or budget < 0:
        raise ValueError("invalid budget")
    if not isinstance(plan, list) or len(plan) > 1000:
        raise ValueError("plan must contain at most 1000 steps")
    seen = {}
    total = Decimal(0)
    rows = []
    for step in plan:
        key = step["id"]
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("invalid or duplicate step id")
        deps = step.get("depends_on", [])
        if not isinstance(deps, list) or not all(isinstance(d, str) and d in seen for d in deps):
            raise ValueError("dependencies must reference earlier steps")
        cost = Decimal(str(step.get("cost", 0)))
        if not cost.is_finite() or cost < 0:
            raise ValueError("invalid cost")
        # Never accept approval assertions from a proposed plan.
        decision = guard.check(step["action"], step["resource"])
        reason = decision["reason"]
        allowed = decision["allowed"]
        if any(not seen[d] for d in deps):
            allowed, reason = False, "dependency-blocked"
        elif allowed and total + cost > budget:
            allowed, reason = False, "budget-exceeded"
        if allowed:
            total += cost
        seen[key] = allowed
        rows.append(dict(id=key, allowed=allowed, reason=reason, cost=str(cost)))
    return dict(ready=all(seen.values()), estimated_allowed_cost=str(total), steps=rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario")
    args = parser.parse_args()
    try:
        with open(args.scenario, encoding="utf-8") as f:
            data = json.load(f)
        result = preflight(data["plan"], Guard(data["subject"], data["grants"], clock=lambda: data["now"]), data["budget"])
        print(json.dumps(result, indent=2))
        return 0 if result["ready"] else 1
    except (OSError, ValueError, TypeError, KeyError, InvalidOperation) as e:
        parser.exit(2, "Invalid scenario: " + str(e) + "\n")
if __name__ == "__main__":
    raise SystemExit(main())
