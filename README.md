# Swagger to Postman Skill

An open Agent Skill that helps an AI agent turn a Swagger/OpenAPI description into a reviewable Postman collection. It inventories the API, asks only for unresolved choices, previews the proposed collection as a tree, waits for approval, and reviews the generated JSON.

## What it does

- Reads a local Swagger 2.0 or OpenAPI 3.x description, or a URL when the agent has authorized network access.
- Organizes the preview as **tag → operation → response scenario**.
- Helps choose collection variables, Postman environments, servers, authentication, and test coverage.
- Distinguishes executable request scenarios from response examples that cannot be triggered reliably.
- Keeps secrets out of generated files and reports unsupported or ambiguous input.
- Guides the agent through an offline structural review of the generated Postman collection.

The skill does not call the API described by the specification. A generated request can have side effects when a person later runs it in Postman; review requests and target environments before execution.

## Install

Copy [`skills/swagger-to-postman/`](skills/swagger-to-postman/) into a supported agent's skills directory, preserving its name and internal paths. Agent skill installation paths differ by product; follow the target agent's official instructions.

## Use

Ask your compatible AI agent to create a Postman collection from a Swagger/OpenAPI file or URL. The skill will:

1. Identify the specification version and inventory operations, servers, security, parameters, bodies, and documented responses.
2. Ask about choices the specification cannot resolve.
3. Show the complete folder/request tree, including scenario type, planned variables/tests, and warnings.
4. Wait for your explicit approval before creating collection or environment files.
5. Review generated collection JSON and summarize assumptions and limitations.

See [the workflow guide](skills/swagger-to-postman/docs/WORKFLOW.md) and [the examples](skills/swagger-to-postman/docs/EXAMPLES.md) for the interaction contract and tree conventions.
Security boundaries are documented in the [security checklist](skills/swagger-to-postman/docs/SECURITY.md). Detailed conversion rules are in the [OpenAPI mapping guide](skills/swagger-to-postman/references/openapi-postman-mapping.md).
Manual security acceptance scenarios are listed in [SECURITY-VERIFICATION.md](skills/swagger-to-postman/docs/SECURITY-VERIFICATION.md).

## Validation

The agent reviews the generated JSON for valid syntax, required collection structure, request methods and URLs, duplicate sibling names, unresolved variables, scenario labels, and source traceability. This uses the agent's available capabilities and does not require a specific programming language or runtime. It does not validate live API behavior or execute requests. Import the result into Postman for an additional compatibility check.

## Supported features and limitations

See [SUPPORTED_FEATURES.md](skills/swagger-to-postman/docs/SUPPORTED_FEATURES.md). The first release targets Swagger 2.0 and OpenAPI 3.x. Vendor extensions and unsupported constructs must be reported. Documented `401`, `404`, or `500` responses do not automatically imply a request that will produce them; the skill must label examples separately from executable scenarios.

## License

MIT. See [LICENSE](LICENSE).
