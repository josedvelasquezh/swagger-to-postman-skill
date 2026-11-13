# Supported Features and Limitations

This first release targets commonly used Swagger/OpenAPI structures and Postman Collection v2.1 JSON. Compatibility claims must be conservative: the skill reports constructs it cannot confidently represent.

| Area | Initial support | Behavior when uncertain |
|---|---|---|
| Swagger/OpenAPI input | Swagger 2.0 and OpenAPI 3.x | Identify dialect; ask for a supported document if parsing fails. |
| Source | One local document or URL | External references need accessible sources; unresolved references are reported. |
| Operations | HTTP methods, paths, tags, operation IDs, summaries | Preserve source traceability; report unsupported operations. |
| Servers | Swagger host/basePath/schemes and OpenAPI servers, including supported overrides | Ask how to represent materially different servers. |
| Parameters | Path, query, header, cookie where representable | Preserve requiredness and explain unsupported serialization styles. |
| Bodies | Media type, schema, required fields, source examples | Do not invent valid bodies when examples are absent. |
| Authentication | Recognized security schemes and operation requirements | Use placeholders; ask only about ambiguity or missing setup. |
| Responses | Documented status codes, schemas, descriptions, examples | Examples are not executable requests unless safe trigger conditions are known. |
| Organization | Tag → operation → scenario; fallback `Other` | Show full tree before writing artifacts. |
| Tests | Optional `pm.test` assertions from documented behavior | Do not infer business rules or claim live verification. |
| Collection format | Postman Collection v2.1 JSON | Validate core structure offline; Postman import remains the final compatibility check. |
| Environments | Optional template(s), placeholders only | Never include actual secret values. |

## Explicit limitations

- The skill does not call, benchmark, or validate behavior against a live API.
- A documented `401`, `404`, or `500` response does not define a reproducible request. A request scenario needs known, approved trigger conditions; otherwise represent the response as an example/documentation case.
- Vendor extensions, complex callbacks/webhooks, links, discriminators, advanced parameter serialization, and unresolved external references may need manual handling. The skill must identify affected operations.
- The validator checks JSON syntax and common structural properties. It is not a full Postman import, OpenAPI semantic validator, or server-side contract test.
- Postman v12 documentation identifies schema 3.0.0 as its current format, while Newman can run exported v2.1.0 collections but not v3.0. This project initially targets v2.1 JSON for compatibility with import and Newman-based runners; evaluate v3 support separately. See [Postman collection schemas](https://learning.postman.com/docs/use/use-collections/collections-schemas).
