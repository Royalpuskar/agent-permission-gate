"""Optional local Ollama adapter. No model installation or tool execution."""
import json
from urllib.request import Request, urlopen

def generate(model, prompt, timeout=60):
    body = json.dumps(dict(model=model, prompt=prompt, stream=False)).encode()
    request = Request("http://127.0.0.1:11434/api/generate", data=body,
                      headers={"Content-Type":"application/json"})
    # Local service must be installed and trusted by the operator.
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read(4_000_000))["response"]
