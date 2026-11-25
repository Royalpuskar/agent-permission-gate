"""Replay synthetic agent requests through the reference policy evaluator."""
import json
import argparse
from engine import analyze

def replay():
    grants = [
        dict(subject="demo-agent", action="read", resource="docs", expires=200, effect="allow"),
        dict(subject="demo-agent", action="send", resource="email", expires=200, effect="allow", approval_required=True),
        dict(subject="demo-agent", action="read", resource="secrets", expires=200, effect="deny"),
    ]
    cases = [
        ("Read documentation", "read", "docs", False, 100, True),
        ("Send email without approval", "send", "email", False, 100, False),
        ("Send email with simulated approval", "send", "email", True, 100, True),
        ("Read protected resource", "read", "secrets", False, 100, False),
        ("Unknown operation", "delete", "docs", False, 100, False),
        ("Expired permission", "read", "docs", False, 200, False),
    ]
    return [dict(label=label, expected=expected, **analyze(dict(now=now, grants=grants, request=dict(subject="demo-agent", action=action, resource=resource, approved=approved)))) for label, action, resource, approved, now, expected in cases]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = replay()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for row in results:
            print(("ALLOW" if row["allowed"] else "DENY ").ljust(7) + row["label"] + " [" + row["reason"] + "]")
    raise SystemExit(0 if all(r["allowed"] == r["expected"] for r in results) else 1)
