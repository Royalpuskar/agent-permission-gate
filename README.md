# Permission Gate

<!-- portfolio-website:start -->
## Website

[Open agent-permission-gate website](https://royalpuskar.github.io/agent-permission-gate/)

GitHub Pages deployment was confirmed during portfolio setup.
<!-- portfolio-website:end -->

**Automation policy workbench · agent-permission-gate · working research prototype**

Evaluate typed automation capabilities with default-deny access.

## Try the 30-second agent replay

```sh
git clone https://github.com/Royalpuskar/agent-permission-gate.git
cd agent-permission-gate
python replay_demo.py
```

Six synthetic requests demonstrate normal access, approval requirements, explicit denial, unknown actions and expired grants. No model, API key or external service is needed. The replay exits nonzero if a decision differs from its expected result; add `--json` for machine-readable output. No actual email, file deletion or secret access occurs.

## Guard your own Python tools

```python
from guard import Guard, PermissionDenied
from tool_gateway import Tool, ToolGateway

policy = [dict(subject="agent", action="read", resource="docs",
               expires=200, effect="allow")]
guard = Guard("agent", policy, clock=lambda: 100)
gateway = ToolGateway(guard, {
    "read_docs": Tool("read", "docs", lambda: "Public documentation")
})
print(gateway.dispatch("read_docs", {}))
```

The dispatcher maps tool names to trusted action/resource metadata. Unknown tools are denied. This is a synchronous local integration example, not an MCP server or an isolation boundary. Handlers must validate their own arguments, and approvals must be provided by trusted application code.

## Inspect a workflow before execution

```sh
python preflight.py workflow_demo.json
python -m unittest test_preflight -v
```

The offline preflight checks ordered dependencies, permission decisions and a caller-supplied estimated budget. The example intentionally exits with status 1 because approval, dependency and budget checks block three steps. No tools are executed, and approval fields in proposed steps are ignored. This is a planning aid, not an enforcement boundary or measured cost guarantee.

## Agent control plane prototype

- [Workflow graph editor](https://royalpuskar.github.io/agent-permission-gate/workflow.html): edit and export dependency graphs (deployment may lag).
- `orchestrator.py`: sequential execution across registered agent gateways; stops dependent steps on failure. No automatic retries or rollback.
- `audit.py`: hash-chain verification against an independently retained digest; not immutable storage.
- `knowledge.py`: local lexical retrieval and illustrative injection flags, not comprehensive prompt-injection protection.
- `policy_draft.py`: approval-required grant drafts for human review.
- `local_model.py`: optional localhost Ollama adapter; model installation is separate.
- `mcp_server.py`: optional read-only MCP example server; install the official SDK with `pip install mcp` and run `python mcp_server.py`. It exposes only the bundled preflight example, not a universal interception gateway.

Run standard-library tests with `python -m unittest discover -v`. Optional service integrations require separate integration testing. All modules are research prototypes; no isolation, certification or production readiness is claimed.

## Problem and approach

Evaluate typed automation capabilities with default-deny access. This project makes the decision process inspectable through editable scenarios, explicit outputs and reproducible examples. It is an independent repository with a browser application and a Python reference implementation.

## Implemented features

Exact action/resource matching; expiry; explicit deny precedence; approval checks; decision explanations.

The responsive website runs locally in your browser, accepts editable JSON scenarios, includes preset cases, renders structured results, and exports a JSON report. It has no external runtime dependencies, analytics, external fonts, model API calls or API-key requirement.

## Run the website

Requires Python 3.10+ for the development server. From this directory:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000`. Use **Run analysis** to evaluate the sample; change a scenario and run again. **Export report** downloads the current result. Serve over localhost or HTTPS so Web Crypto is available. Opening `index.html` directly as a file is not supported because the application uses JavaScript modules.

## Command-line usage

```sh
python engine.py sample.json
```

`sample.json` documents the accepted example shape; `expected.json` contains its expected output. `cases.json` adds fixed expected outcomes for boundary and normal cases.

## Tests

Python 3.10+ and Node.js 22+; no package installation:

```sh
python -m unittest -v
node test.mjs
```

The suites check explicit expected outcomes and input immutability. The JavaScript suite also checks malformed top-level inputs and reserved keys. Browser and Python results are compared against the same contract fixtures. Passing these cases is not a security certification or a claim of comprehensive coverage.

## Architecture

| File | Responsibility |
| --- | --- |
| `index.html`, `style.css` | Accessible responsive workbench |
| `app.mjs` | Scenario controls, safe DOM rendering, report export |
| `engine.mjs` | Browser-side algorithm |
| `engine.py` | Independent Python reference and CLI |
| `config.mjs` | Project identity and sample scenarios |
| `cases.json` | Explicit input/output contracts |

Flow: user edits a scenario → JSON parsing and bounded-input checks → project algorithm → text-only result rendering → optional user-triggered report download. There is no application server, account system or backend database.

## Security, privacy and limitations

Local policy evaluator, not an authentication server. Approval booleans are fixture inputs; a real deployment must obtain verified approvals from a trusted service.

Scenario data stays in browser memory. The app makes no analysis network requests and stores no inputs in local storage. A hosting provider can still receive ordinary page requests and access logs. Avoid entering real secrets or sensitive evidence; downloaded reports contain your input and results. HTML from scenarios is rendered as text, never executed. Limits cap browser inputs at 100 KB, 1,000 array elements and 15 nesting levels; these limits are prototype safeguards, not a complete denial-of-service defense.

## Development roadmap

- Expand adversarial and boundary fixtures before adding new capabilities.
- Add project-specific form controls alongside the advanced JSON editor.
- Measure performance with published datasets and reproducible methods.
- Conduct independent accessibility and security review.
- Document any integrations before introducing network calls or data retention.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [LICENSE](LICENSE). Changes should include a concrete failing case and an explanation of assumptions. No benchmark, adoption or certification claims are made without supporting evidence.


<!-- portfolio-rights:start -->
## Copyright

© 2026 Puskar (Royalpuskar). All rights reserved except the permissions expressly granted by this repository’s MIT License. Third-party rights and notices remain with their owners.
<!-- portfolio-rights:end -->
