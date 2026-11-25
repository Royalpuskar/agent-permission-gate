"""In-memory hash-chain audit. Export and anchor the final digest externally."""
import hashlib
import json

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()

class Audit:
    def __init__(self):
        self.entries = []

    def append(self, step, status):
        row = dict(index=len(self.entries), step=step, status=status,
                   previous=self.entries[-1]["hash"] if self.entries else "0"*64)
        row["hash"] = digest(row)
        self.entries.append(row)
        return row["hash"]

def verify(entries, anchor):
    previous = "0"*64
    for i, row in enumerate(entries):
        body = {k:v for k,v in row.items() if k != "hash"}
        if body.get("index") != i or body.get("previous") != previous or digest(body) != row.get("hash"):
            return False
        previous = row["hash"]
    return previous == anchor
