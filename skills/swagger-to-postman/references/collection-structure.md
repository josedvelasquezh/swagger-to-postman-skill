# Collection Structure Conventions

## Hierarchy

Use folders in this order:

1. API tag or user-approved group.
2. Operation folder named from `operationId`, then summary, then a stable `METHOD path` fallback.
3. Scenario requests with status and description in the request name. Label documentation-only cases as `[example]` in the preview; do not disguise them as executable requests.

Operations without tags go in `Other`. Preserve multiple tags only if that does not duplicate executable requests unexpectedly; otherwise ask whether to select a primary tag or duplicate the operation into each tag folder.

## Names and order

- Preserve source wording where clear; normalize whitespace and avoid unstable generated suffixes.
- Include method and path in the operation preview for disambiguation.
- Sort folders by source tag order, then stable alphabetical fallback. Keep operation order stable by source document order or a documented stable sort.
- Detect duplicate request names within sibling folders and disambiguate with method/path, not random IDs.

## URLs, servers, and variables

- Represent selectable host/base URL using a variable such as `{{baseUrl}}` when appropriate.
- Explain collection variables versus environments. Environments are selectable configurations; use placeholders and omit secrets.
- If an operation has a server override, show it in the preview and preserve it without silently replacing it with the root server.
- URL encode path/query values according to their declared serialization rules where supported. Report unsupported styles.

## Authentication and tests

- Follow the source security requirement and scope it at collection/folder/request level only when this accurately represents the specification.
- Use variable references for API keys, bearer tokens, and credentials; never populate secret values.
- Add tests only when requested. Status assertions must correspond to the chosen executable scenario. Response-body assertions need source-defined examples or schema-grounded expectations.
- Do not create pre-request scripts that fetch tokens or mutate external state unless the user explicitly asks and provides a safe design.

## Traceability and descriptions

Add a concise description with the source path, method, and operation identifier when available. Keep generated names stable and avoid storing the full source document in each request.
