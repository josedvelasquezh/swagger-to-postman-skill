# Implementation Plan: Swagger to Postman Skill

## Project objective

Create a public, English-language Agent Skill that turns a Swagger/OpenAPI description into a well-organized, reviewable Postman collection. The skill must inspect the specification, ask only for decisions it cannot safely infer, preview the proposed collection as a tree, wait for explicit approval, then generate and validate the collection and any requested environment template.

The first release is complete when a new user can provide a supported API description, understand the generated structure and its assumptions, approve it, import the resulting collection into Postman, and see clear validation results and limitations.

## Product decisions

- Repository: `swagger-to-postman-skill`, public on GitHub.
- License: MIT. Include the full license text and explain reuse and attribution in the README.
- Skill and repository documentation: English.
- Git workflow: `develop` is the integration branch during implementation; `main` receives the reviewed release. Use short-lived feature branches from `develop` when useful. Do not develop directly on `main`.
- Commit messages: English, Conventional Commits style, for example `feat: add scenario preview` and `docs: document variable strategy`.
- Input: a local Swagger/OpenAPI file or a URL, subject to the runtime's access and file permissions.
- Initial format support: Swagger 2.0 and OpenAPI 3.x. Unsupported or ambiguous constructs must be reported rather than silently dropped.
- Collection organization: tags → operation → response scenario. Untagged operations go under `Other` unless the user approves another grouping rule.
- Collection format: Postman Collection v2.1, unless implementation research identifies a concrete compatibility blocker.
- The skill generates artifacts; it does not send requests to the target API.

## Golden rules

1. **Inspect first.** Read the complete supplied specification and resolve its references before proposing output. State which file/URL and format version were read.
2. **Ask only material questions.** Present detected facts first. Ask for decisions the specification cannot answer, such as environment strategy, server selection, test depth, and whether response scenarios should be executable requests or documentation examples.
3. **Never invent API behavior.** Do not fabricate required fields, valid identifiers, credentials, server URLs, response payloads, or expected status codes. Mark missing data as a placeholder or unresolved assumption and explain it.
4. **Separate response examples from executable scenarios.** A response code such as 401, 404, or 500 does not by itself describe a request that will produce it. Make the distinction visible in the tree and in the generated collection. Generate an executable scenario only when the request conditions are specified or approved; otherwise include a clearly labeled Postman example/documentation case if the collection format supports it.
5. **Preview before writing.** Show the complete proposed folder/request tree, counts, variable plan, test plan, and unresolved warnings. Do not create final artifacts until the user explicitly approves that preview.
6. **Keep credentials out of artifacts.** Use placeholders for secrets. Never copy credentials from the prompt, environment, source files, or local configuration into the collection or an exported environment template.
7. **Preserve traceability.** Each request and warning should be traceable to its source operation (tag, method, path, and `operationId` when available).
8. **Be deterministic.** The same specification and choices should produce stable names, folder order, and output, except where the source itself changes.
9. **Validate before declaring success.** Parse generated JSON, validate the collection structure, check references/variables and report what was or was not validated. Never claim a request was tested against a live API.
10. **Make limits visible.** Report unsupported constructs, unresolved references, omitted operations, and assumptions in a concise completion summary.
11. **Keep the skill portable.** Use the Agent Skills format and avoid dependencies on a single editor or proprietary API unless required and documented.
12. **Keep changes reviewable.** Work on `develop`, use focused English commits, review the finished branch, then merge the completed release into `main`.

## User workflow and interaction contract

### 1. Intake

Accept a local file or URL. Identify whether it is Swagger 2.0 or OpenAPI 3.x. Ask for a supported source if parsing fails. Record the source name, detected version, and whether external references are present.

### 2. Analysis

Build an inventory of operations, tags, servers/base URLs, security schemes, parameters, request bodies, documented responses, examples, and unresolved references. Detect duplicate or missing operation identifiers, unsupported schema constructs, and likely sensitive example values. Do not expose secrets in logs or summaries.

### 3. Clarifying questions

Ask concise questions with detected values and recommended defaults. Cover these dimensions when they are relevant:

- **Variables and environments:** collection variables, one or more Postman environments, or both. Explain that deployment environments (local/staging/production) differ from separate API servers.
- **Servers:** use one selected server, provide a selectable variable for alternatives, or keep separate server groups when operations genuinely target different hosts. Respect server overrides at the operation/path level where supported.
- **Tests:** whether to add `pm.test` checks; select documented status checks only or additional response-body/schema checks when evidence exists.
- **Response coverage:** all documented response codes or a selected subset; distinguish checks/examples from executable negative-test requests.
- **Auth:** confirm detected scheme and ask only for missing configuration. Use variable placeholders for secrets.
- **Folder grouping:** tags, path segments, or a user-defined grouping when tags are absent/unsuitable.
- **Examples:** whether to use examples already in the specification; ask before generating synthetic values.

Do not force irrelevant questions. If the specification has one server, no authentication, or no response examples, explain the detected condition and ask only where a user choice remains.

### 4. Preview and approval gate

Before artifact generation, show:

- A full tree of folders, operations, and scenarios, with HTTP method, path, expected status, and counts.
- A legend that distinguishes executable requests from response examples/documentation-only cases.
- Variable and environment names, with secret values omitted.
- Planned test assertions and any assumptions.
- Warnings, unsupported constructs, and operations that will be omitted or need manual input.

Example preview:

```text
Swagger to Postman Collection (18 requests, 2 examples)
├── Customers (8 requests)
│   ├── Get customer by ID [GET /customers/{customerId}]
│   │   ├── 200 — Customer found [request]
│   │   ├── 401 — Unauthorized [example; executable only if auth setup is confirmed]
│   │   └── 404 — Customer not found [request; requires approved missing-ID strategy]
│   └── Create customer [POST /customers]
│       ├── 201 — Customer created [request]
│       └── 400 — Invalid request [example; no invalid body defined]
└── Other (1 request)
    └── Health check [GET /health]
```

Wait for explicit approval or requested edits. If the user changes choices, regenerate the preview and obtain approval for the changed tree before writing final files.

### 5. Generation

After approval, generate the Postman collection and only the optional environment template(s) the user requested. Use Postman variables for configurable values, stable request names, and source-derived descriptions. Create separate requests for executable scenarios only when their inputs and expected behavior are grounded in the spec or user-approved. Keep examples/documentation-only cases visibly labeled and do not imply they execute a test.

### 6. Validation and handoff

Validate JSON syntax and the supported Postman Collection schema. Check duplicate request names within a folder, unresolved variables, missing URLs/methods, and traceability to source operations. Summarize files created, counts, validation results, assumptions, skipped operations, and manual follow-up. State explicitly that no live API calls were made.

## Recommended output tree

```text
Postman Collection
├── <Tag or approved group>
│   └── <Operation name> [METHOD /path]
│       ├── <status> — <response description> [request or example]
│       └── ...
└── Other
```

Each response node is either an independently executable request scenario or a documentation/example case. The preview must label which kind it is. Do not imply that a Postman folder is an API operation; the operation folder groups its scenario requests.

## Repository structure target

```text
swagger-to-postman-skill/
├── skills/
│   └── swagger-to-postman/     # Installable Agent Skill directory (matches SKILL.md name)
│       ├── SKILL.md            # Main instructions and workflow
│       ├── docs/
│       ├── examples/
│       ├── references/
│       └── examples/
├── README.md                   # English user-facing overview, install/use, examples
├── LICENSE                     # MIT license
└── CHANGELOG.md                # User-visible changes by release
```

Keep `SKILL.md` focused on the ordered workflow and golden rules. Put branch-specific reference material in `references/` and point to it from `SKILL.md` exactly where the agent needs it. Keep examples small and representative; avoid duplicating rules across README, skill, and references.

## Phases and acceptance criteria

### Phase 1 — Repository foundation and product contract

**Work:** Confirm repository naming, Agent Skills packaging, supported specification versions, Postman output format, MIT licensing, and workflow boundaries. Create the public GitHub repository and `develop` branch after plan approval. Add the initial directory structure, license, README skeleton, and contribution/commit conventions.

**Acceptance criteria:**

- The public repository is named `swagger-to-postman-skill` and has MIT license text.
- `develop` is the working integration branch; `main` is reserved for reviewed releases.
- README clearly states purpose, inputs, outputs, safety boundaries, and current support level.
- The product contract distinguishes collection generation from live API execution.

**Checkpoint:** Review the repository scaffold and scope before implementing behavior.

### Phase 2 — Skill instructions and guided interaction

**Work:** Write `SKILL.md` with metadata, trigger/use cases, ordered intake-analysis-question-preview-approval-generation-validation flow, safety rules, and references to branch-specific documentation. Define concise prompts and recommended defaults.

**Acceptance criteria:**

- A new agent can follow the steps in order without relying on this conversation.
- It asks only relevant questions and displays detected facts before asking.
- It has a hard approval gate between preview and artifact generation.
- It distinguishes response assertions, response examples, and executable scenarios.
- It never includes secrets or claims live execution.

**Checkpoint:** Walk through the workflow against the examples before adding broader format coverage.

### Phase 3 — Collection model and scenario rules

**Work:** Specify request naming, tag/path grouping, server and environment resolution, authentication variables, request construction, response handling, `pm.test` strategy, and handling of unsupported/ambiguous constructs. Define when a response status can and cannot become an executable scenario.

**Acceptance criteria:**

- Tree shape is tags → operation → scenario, with a documented fallback for missing tags.
- Every scenario preview identifies method/path/status and whether it is executable or example-only.
- Expected status assertions come from the source or an explicit user choice.
- No invalid payload, fake identifier, or error-triggering input is fabricated as a guaranteed scenario.
- Multi-server behavior distinguishes alternate deployments from distinct API hosts.

### Phase 4 — Generation and validation support

**Work:** Define a language-agnostic structural review checklist for the agent. Keep validation offline and limited to claims it can prove. Do not require a local runtime or technology-specific script.

**Acceptance criteria:**

- Generated collection JSON parses and satisfies the agent's documented core v2.1 structural review checklist; it is not represented as full JSON Schema validation.
- Review checks unresolved variables, missing method/URL, duplicate names, scenario labels, and source traceability where possible.
- Review does not require a local runtime, make network calls, or execute collection requests.
- The completion report separates errors, warnings, and informational limits.
- A representative collection fixture is checked against Postman's official v2.1 JSON Schema during release review; actual server behavior is outside the release verification scope.

### Phase 5 — Examples, documentation, and adversarial review

**Work:** Add representative fixtures for basic APIs, multiple servers, security, multiple documented statuses, missing tags/examples, external references, and unsupported constructs. Document installation, invocation, workflow, examples, supported features, and limitations. Review for confusing or unsafe behavior.

**Acceptance criteria:**

- Each major decision branch has at least one fixture and expected preview/output notes.
- Documentation is English, consistent with `SKILL.md`, and includes a complete walkthrough.
- Examples contain no real secrets or production endpoints.
- Review catches silent omission, invented assumptions, misleading scenario labels, and inconsistent tree output.

**Checkpoint:** The skill and docs are reviewed on `develop`; unresolved issues are listed before release.

### Phase 6 — Release to `main`

**Work:** Confirm all planned files are present, run the documented validation and fixture checks, review the final diff and commit history, update changelog/version, then merge the completed `develop` work into `main` and publish the initial public release.

**Acceptance criteria:**

- All phase acceptance criteria are satisfied or explicitly recorded as deferred.
- The final branch contains no secrets, local paths, or uncommitted changes.
- Commits are English and use the agreed format.
- `main` contains the reviewed release and the GitHub repository is public.
- Release notes describe capabilities, limitations, and how to install/use the skill.

## Verification strategy

- Validate the skill package metadata and referenced files.
- Review the representative collection fixture and an invalid example against the structural checklist.
- Check preview snapshots for deterministic ordering and clear scenario labels.
- Manually walk through at least one case with a single server, one with multiple servers, and one with 200/401/404/500 responses.
- Confirm the approval gate by checking that no final collection artifact is written before preview approval.
- Verify no fixture or generated output contains credentials or claims of live API testing.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| A response code is mistaken for a reproducible test case | Label executable requests vs examples; require grounded input conditions or user approval. |
| OpenAPI dialect differences cause silent omissions | Maintain a support matrix and report unsupported constructs per operation. |
| Multiple `servers` are confused with deployment environments | Explain the distinction and preview the selected mapping. |
| Generated requests cause side effects if run against real APIs | Never execute requests; mark potentially mutating operations and keep examples explicit. |
| Skill instructions become too long and inconsistent | Keep the main workflow in `SKILL.md`; disclose details into focused reference files. |
| Dependency or schema changes break validation | Pin versions and document the supported collection schema/version. |

## Deferred from the first release

- Executing requests against live services.
- Creating or managing Postman workspaces through external APIs.
- Inventing realistic production data or credentials.
- Guaranteeing that error scenarios will return a particular status without a test server or API-specific setup.
- Supporting every vendor extension or every OpenAPI edge case.

## Definition of done

The first release is done when the public MIT-licensed repository on `main` contains a usable English Agent Skill, clear documentation and examples, a reviewed preview/approval workflow, documented support limits, and repeatable offline validation; the `develop` history shows organized English commits, and the skill never silently invents behavior or leaks secrets.
