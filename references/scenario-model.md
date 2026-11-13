# Scenario Model

## Why scenarios need two kinds

An OpenAPI response describes what an operation may return. It does not necessarily describe request input that will cause that response. For example, a documented `404` does not say which identifier is absent, and a `500` is generally not safe or deterministic to trigger.

Represent each response case as one of:

- **Request scenario:** an independently executable Postman request with known inputs and an expected status grounded in the specification or explicitly approved by the user. Running it may have side effects.
- **Response example:** documentation associated with an operation, using a source-provided response example/schema. It is not a runnable assertion and must be labeled as such.

If Postman cannot represent the desired documentation case as a non-runnable item in the chosen collection structure, keep it in the preview/report and do not create a misleading request. Explain the limitation.

## Tree convention

```text
<Tag or approved group>
└── <Operation summary> [METHOD /path]
    ├── 200 — <description> [request]
    ├── 401 — <description> [example]
    └── 404 — <description> [request, user-approved trigger]
```

Folders group operations and scenarios; scenario labels identify expected outcomes. When an operation has multiple examples for one status, use stable distinguishing labels from the source example names or media types.

## Scenario construction rules

- Use the operation's effective server, path, security, and parameters.
- Use only source-provided or user-approved values. Use Postman variables for configurable IDs and hosts.
- For a negative request, state exactly what makes the input negative and why that should produce the expected response. If the spec gives no trigger, use an example-only case or ask the user.
- Never create a `500` request by corrupting production data or causing a failure. Treat it as an example unless a controlled test environment and a specific safe trigger are provided.
- Include a `pm.test` status check only if the user requested tests and the scenario is executable. For example cases, keep response payload samples as documentation and do not add assertions implying they ran.
- Do not generate extra duplicate requests just to enumerate responses when the user's requested output is status assertions on one request. Clarify the desired coverage.
