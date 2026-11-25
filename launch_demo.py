"""Run a synthetic, side-effect-free agent control plane demonstration."""
import json
from guard import Guard
from tool_gateway import Tool, ToolGateway
from orchestrator import execute
from audit import verify
from policy_draft import draft

def demo():
    requests = [{"action":"read","resource":"docs"},{"action":"publish","resource":"report"}]
    grants = draft("researcher", requests, 200)
    grants[0]["approval_required"] = False if grants[0]["action"] == "read" else True
    for grant in grants:
        if grant["action"] == "read":
            grant["approval_required"] = False
    effects = []
    gateway = ToolGateway(Guard("researcher", grants, clock=lambda:100), {
        "read":Tool("read","docs",lambda:effects.append("read")),
        "publish":Tool("publish","report",lambda:effects.append("publish"))
    })
    plan = [{"id":"research","agent":"researcher","tool":"read"},
            {"id":"publish","agent":"researcher","tool":"publish","depends_on":["research"]}]
    states, entries = execute(plan, {"researcher":gateway})
    assert effects == ["read"]
    assert states == {"research":"completed","publish":"failed"}
    assert verify(entries, entries[-1]["hash"])
    return {"states":states,"synthetic_effects":effects,"audit_verified":True,"audit":entries}

if __name__ == "__main__":
    print(json.dumps(demo(),indent=2))
