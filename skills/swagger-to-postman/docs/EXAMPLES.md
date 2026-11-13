# Examples

These examples define interaction expectations. They are intentionally small and contain no real credentials or production hosts.

## Multiple documented responses

Input operation: `GET /customers/{customerId}` with documented 200, 401, 404, and 500 responses, but no example missing ID or server-failure trigger.

Expected preview:

```text
Customers
└── Get customer by ID [GET /customers/{customerId}]
    ├── 200 — Customer returned [request; status test if selected]
    ├── 401 — Unauthorized [example unless auth-negative input is approved]
    ├── 404 — Customer not found [example; no missing-ID trigger defined]
    └── 500 — Internal server error [example; no safe deterministic trigger]
```

The skill asks whether the user has safe, test-environment-specific inputs for executable negative scenarios. It does not invent a customer ID or induce a server failure.

## Multiple deployment environments

If the source has one server and the user wants local/staging/production, explain that these are environment values for one API. Offer a `{{baseUrl}}` variable and an environment template with blank/placeholders, according to the user's choice.

## Multiple API servers

If operations use different hosts, show which operations map to each host. Ask whether to keep separate groups or use distinct variables. Do not collapse unrelated hosts into one `baseUrl` silently.

## Preview changes

If the user changes from “all response cases” to “only 2xx status assertions,” update counts and tree, explain which error examples are excluded, and request approval for the updated preview before writing files.

## Fixture index

- [`openapi-basic.yaml`](../examples/openapi-basic.yaml): one tagged operation with a source example.
- [`openapi-multiple-servers.yaml`](../examples/openapi-multiple-servers.yaml): root and operation-level server choices.
- [`openapi-missing-tags-examples.yaml`](../examples/openapi-missing-tags-examples.yaml): untagged operation without a request/response example; expected to use `Other` and ask before inventing payloads.
- [`openapi-external-reference.yaml`](../examples/openapi-external-reference.yaml): external schema reference; report unresolved reference when the referenced file is unavailable.
- [`openapi-unsupported-construct.yaml`](../examples/openapi-unsupported-construct.yaml): callback and vendor extension; report limits rather than silently omitting behavior.
- [`openapi-auth-and-errors.yaml`](../examples/openapi-auth-and-errors.yaml): auth and multiple responses; expected tree is recorded in [`expected-preview.txt`](../examples/expected-preview.txt).
- [`postman-collection-v2.1.json`](../examples/postman-collection-v2.1.json): representative collection with a request, a test, variables, and a saved response example.
