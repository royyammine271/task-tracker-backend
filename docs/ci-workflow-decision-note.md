# Technical Decision Note: CI Workflow Design for Module 4

## Context

Module 4 required clear evidence that automated checks run on every code change and fail when tests fail. The Task Tracker is a learning project with FastAPI, Pydantic, JSON file storage, and a simple frontend. The immediate need was a reliable quality gate without adding scope beyond the module.

## Decision

Use one GitHub Actions workflow that runs on `push` and `pull_request`, uses Python `3.11`, installs dependencies from `requirements.txt`, and runs `pytest -v` as the required gate.

## Alternatives Considered

1. Skip CI and rely only on local test runs.
2. Use a Python version matrix across multiple versions.
3. Add lint, type-checking, and security scanning in this same module.
4. Add Docker build checks to CI.
5. Add deployment stages after tests pass.

## DRAFT - REWRITE IN MY OWN WORDS Trade-offs

- The workflow is easy to understand and maintain, but validates only one Python version path.
- It catches test regressions early, but does not yet cover linting or type checks.
- It fits module scope, but is not a complete production CI policy.

I would do this differently by adding one additional gate at a time after this baseline is stable, starting with a Docker build check.

## Consequences

Positive:

- Every push and pull request gets an automated pass/fail signal.
- Test failures are visible immediately in CI.
- Evidence for module grading is straightforward to collect.

Negative:

- No automated lint/type/security checks yet.
- No CI verification yet for Docker runtime behavior.
- Cross-version Python issues may go undetected.

## DRAFT - REWRITE IN MY OWN WORDS Open Questions

- Should the next module add a Docker build job to CI without adding deployment?
- Should dependency versions be pinned more strictly for reproducibility?
- Should a lightweight lint or type-check step be added now, or deferred?