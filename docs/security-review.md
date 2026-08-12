# Module 5 Security Review

## Reconciliation Table

| Agreement | AI-only | You-only |
| S-01 Unbounded user text fields (accepted as Valid in grading pass). | S-04 Local CORS/frontend base URL assumption (kept as Noise in grading pass). | None provided in grading notes. needs evidence |
| S-02 No auth/authorization outside course scope (accepted as Valid production risk in grading pass). | S-06 CI lacks security scan steps (kept as Noise for this module in grading pass). | None provided in grading notes. needs evidence |
| S-03 Storage I/O and JSON parse exceptions can bubble as server errors (accepted as Valid in grading pass). |  |  |
| S-05 Unpinned dependencies / CI drift risk (accepted as Valid in grading pass). |  |  |

## Coverage Observation

AI coverage was strongest on baseline backend and supply-chain hygiene risks (validation bounds, auth absence, exception handling, dependency pinning).
AI also produced environment/scope-noise items; the grading pass added context filtering that kept the backlog focused on actionable Module 5 work.

## Top-3 Security Backlog (Valid Findings)

| Rank | Finding | Why it matters | Suggested owner | Next action |
| 1 | S-05 Unpinned dependencies and CI drift | Reproducibility and supply-chain stability can change between runs without code changes. | DevOps + backend | Pin versions in dependency file and re-run CI to confirm deterministic installs. |
| 2 | S-01 Unbounded description/assignee/comment fields | Large payloads can increase storage/API pressure and create abuse surface. | Backend | Add explicit max length constraints and tests for over-limit inputs. |
| 3 | S-03 Storage read/write exceptions not normalized at API boundary | Malformed data or file I/O faults can surface as uncontrolled 500 paths. | Backend | Add controlled exception handling and stable API error responses for storage failures. |

## Grader-Style Finding Classification

| Finding ID | My grade | Why I graded it this way | Evidence used |
| S-01 | Valid | The issue is real in this repo: title is bounded, but other user-controlled text fields are not explicitly bounded, which could allow oversized payload/storage growth outside classroom use. | [app/models.py](app/models.py#L24), [app/models.py](app/models.py#L27), [app/models.py](app/models.py#L110), [app/models.py](app/models.py#L117) |
| S-02 | Valid | No authentication is intentionally out of scope for this course project, but it is still a legitimate production-risk finding if this app were exposed beyond class context. | [app/main.py](app/main.py#L77), [app/main.py](app/main.py#L109), [app/main.py](app/main.py#L214), [README.md](README.md#L125), [AGENTS.md](AGENTS.md#L85) |
| S-03 | Valid | Storage I/O and parsing are not wrapped in controlled API-level error handling, so malformed JSON or file write/read failures can surface as server errors. | [app/storage.py](app/storage.py#L21), [app/storage.py](app/storage.py#L31), [app/main.py](app/main.py#L71) |
| S-04 | Noise | This is technically true, but mostly a local-environment assumption (localhost CORS and frontend base URL). It is not a strong Module 5 action item unless we are grading for production hardening. | [app/main.py](app/main.py#L46), [app/main.py](app/main.py#L47), [frontend/index.html](frontend/index.html#L616) |
| S-05 | Valid | Dependencies are unpinned, and CI installs floating versions. That is a real reproducibility and supply-chain drift risk. | [requirements.txt](requirements.txt), [.github/workflows/ci.yml](.github/workflows/ci.yml#L20) |
| S-06 | Noise | True but generic: CI currently tests only with pytest by design. This is not a defect by itself for this module unless security scanning is explicitly required. | [.github/workflows/ci.yml](.github/workflows/ci.yml#L1), [.github/workflows/ci.yml](.github/workflows/ci.yml#L26), [README.md](README.md#L95) |

Final grader note:
I treated no-auth as a valid production risk while still acknowledging it as intentional course scope. I did not upgrade severity without repo evidence.
