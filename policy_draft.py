"""Draft least-scope grants for human review; never applies policies."""
def draft(subject, requests, expires):
    pairs = sorted({(r["action"], r["resource"]) for r in requests})
    return [dict(subject=subject, action=a, resource=r, expires=expires,
                 effect="allow", approval_required=True) for a,r in pairs]
