# Swagger to Postman Skill

An open Agent Skill that helps an AI agent turn a Swagger/OpenAPI description into a reviewable Postman collection. It inventories the API, asks only for unresolved choices, previews the proposed collection as a tree, waits for approval, and validates the generated JSON.

## What it does

- Reads a local Swagger 2.0 or OpenAPI 3.x description, or a URL when the agent has authorized network access.
- Organizes the preview as **tag → operation → response scenario**.
- Helps choose collection variables, Postman environments, servers, authentication, and test coverage.
- Distinguishes executable request scenarios from response examples that cannot be triggered reliably.
- Keeps secrets out of generated files and reports unsupported or ambiguous input.
- Provides an offline structural validator for Postman Collection v2.1 JSON.

The skill does not call the API described by the specification. A generated request can have side effects when a person later runs it in Postman; review requests and target environments before execution.

## Install

Copy this repository's `SKILL.md` and its sibling `scripts/` and `references/` directories into a supported agent's skills directory, preserving their relative paths. Agent skill installation paths differ by product; follow the target agent's official instructions.

## Use

Ask your compatible AI agent to create a Postman collection from a Swagger/OpenAPI file or URL. The skill will:

1. Identify the specification version and inventory operations, servers, security, parameters, bodies, and documented responses.
2. Ask about choices the specification cannot resolve.
3. Show the complete folder/request tree, including scenario type, planned variables/tests, and warnings.
4. Wait for your explicit approval before creating collection or environment files.
5. Validate generated collection JSON and summarize assumptions and limitations.

See [the workflow guide](docs/WORKFLOW.md) and [the examples](docs/EXAMPLES.md) for the interaction contract and tree conventions.

## Validate a collection

Python 3.10+ is required. The validator uses only the Python standard library and makes no network calls.

```powershell
python scripts/validate_collection.py path\to\collection.json
```

It checks JSON syntax and core v2.1 structure, request method/URL, duplicate sibling names, and reports variables used in request definitions that are not declared at collection scope (they may be supplied by an environment). Scenario labels and source traceability are part of the skill's manual review, not checks performed by this script. It is a structural validator, not a substitute for importing the collection into Postman or running requests.

## Supported features and limitations

See [SUPPORTED_FEATURES.md](docs/SUPPORTED_FEATURES.md). The first release targets Swagger 2.0 and OpenAPI 3.x. Vendor extensions and unsupported constructs must be reported. Documented `401`, `404`, or `500` responses do not automatically imply a request that will produce them; the skill must label examples separately from executable scenarios.

## License

MIT. See [LICENSE](LICENSE).
