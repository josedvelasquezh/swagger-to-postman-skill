# OpenAPI to Postman Mapping Rules

Use these rules before proposing a collection. Follow the source dialect; do not infer omitted values as though they were explicit.

## Operation and folder model

- Create one Postman operation folder per HTTP operation, grouped by primary tag. Untagged operations go in `Other`.
- Keep response scenarios beneath that operation in the preview. Executable cases become separately named requests only with known safe inputs; documented payloads become saved Postman response examples on the operation request, not fake executable requests.
- Stable operation name precedence: `operationId`, summary, then `METHOD path`. Preserve method, path, and source pointer in the description.

## Servers and URLs

- OpenAPI 3.x: effective server precedence is operation-level, then path-level, then root-level; use the default relative `/` server only when no `servers` value exists at any applicable level.
- Swagger 2.0: construct base URL from `schemes`, `host`, and `basePath`; when absent, preserve the documented relative/default behavior and ask if it cannot be determined safely.
- Server variables become Postman variables with declared defaults. Show alternative servers distinctly; never merge unrelated hosts into one base URL.
- Append the path template without losing path separators or server base paths. Preserve path placeholders as `{{variableName}}` and encode values at runtime according to the parameter serialization rules.

## Parameters

- Combine path-item parameters with operation parameters by `(name, in)`; operation-level entries override matching path-item entries. Preserve requiredness, description, schema/type, default, and example.
- Path parameters are required and become URL path variables. Query parameters become query entries; headers become headers; cookie parameters become a `Cookie` header only when representable. Do not duplicate auth parameters already supplied by Postman auth.
- OpenAPI 3.x: honor `style`, `explode`, `allowReserved`, and `content`; apply defaults only as specified by the dialect. Swagger 2.0: honor `collectionFormat`, `allowEmptyValue`, and `type`/`items` rules.
- If a serialization mode cannot be represented faithfully, mark it unsupported and ask before choosing a lossy representation.

## Request bodies and media types

- OpenAPI 3.x: use `requestBody.content` media type, `required`, schema, and named examples. Swagger 2.0: interpret `body`, `formData`, `consumes`, and `in: body`/`in: formData` according to the source version.
- Choose a content type only when the spec or a unique supported media type makes it unambiguous. Handle JSON, URL-encoded, and multipart distinctly; never hand-set a multipart boundary.
- Build sample bodies from source examples. If only a schema exists, ask whether to create clearly synthetic placeholders; never present them as valid business data.
- Preserve binary/file inputs as placeholders and explain the manual file selection required in Postman.

## Security and authentication

- OpenAPI security requirement objects are OR alternatives; schemes within one requirement object are AND requirements. Operation-level `security` overrides root security, including an empty list (no auth) or an empty object (optional auth).
- Swagger 2.0 security definitions and operation requirements follow their v2 semantics. Convert only schemes Postman can represent; report unsupported schemes and scopes.
- Place auth at collection/folder/request scope only when it preserves the effective per-operation requirements. Use variable placeholders for every credential.

## Responses and tests

- Include documented response codes, descriptions, media types, headers, schemas, and named examples in the analysis and preview.
- A status code alone is not a trigger. Use saved Postman response examples for concrete documented payloads; use an executable scenario only with explicit safe request conditions.
- `pm.test` assertions must reflect the selected request scenario and documented behavior. Do not add a `500` assertion to an ordinary happy-path request or infer response-body assertions from descriptions alone.
- Distinguish unsupported, absent, and intentionally omitted response information in the final report.

## Dialect and uncertainty

Swagger 2.0, OpenAPI 3.0, 3.1, and 3.2 have meaningful differences. Record the detected version. Apply only matching rules. For unsupported schema dialect features, callbacks, links, discriminators, webhooks, or vendor extensions, show the affected operations and leave behavior unresolved rather than silently approximating it.

Primary references: [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3), [OpenAPI 3.1.2](https://spec.openapis.org/oas/v3.1), and [OpenAPI 3.2.1](https://spec.openapis.org/oas/latest.html).
