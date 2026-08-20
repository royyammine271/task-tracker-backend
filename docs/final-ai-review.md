# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| In changed file `app/storage.py` (commit `dd6d710`), `_load_tasks()` has no defensive handling for malformed JSON and could fail startup or request paths hard; recommend controlled exception handling at API boundary. | Useful | This is a real reliability risk in code paths that load persisted data and can surface as 500 responses. | Kept as a valid review finding; verified by tracing `_load_tasks()` usage through list/get/update/delete flows in code and confirming no explicit error normalization in route handlers. |
| In changed file `app/storage.py`, `add_comment()` stores comments as plain strings without length limits; recommend a max length guard to prevent oversized payload persistence and UI rendering strain. | Useful | This is a code-level input hardening suggestion tied to existing comment persistence behavior. | Kept as a scoped improvement note; verified current validator only strips/blank-checks in `TaskCommentCreate` and does not enforce a size cap. |
| In changed file `app/main.py`, `delete_task_comment()` correctly distinguishes missing task vs invalid comment index and returns separate 404 details; keep this behavior and ensure tests lock it in. | Useful | This is a positive review comment on error-contract correctness and helps prevent regressions. | Kept and verified against tests covering missing task and invalid index response details. |
| In changed file `app/storage.py`, suggestion to replace JSON file persistence with a database now is out of scope for this course module and current architecture. | Noise | It is an architectural expansion, not a focused code review action for the current diff and requirements. | Rejected for this submission scope; retained JSON persistence and existing API contracts. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| Unpinned dependencies and CI drift | [requirements.txt](../requirements.txt), [.github/workflows/ci.yml](../.github/workflows/ci.yml) | Valid | Floating dependency installs can change behavior and create reproducibility risk. | Pin dependency versions and verify CI remains stable. |
| Unbounded user-controlled fields | [app/models.py](../app/models.py) | Valid | Text inputs are not explicitly bounded in the same way as some other validation fields. | Consider max-length constraints if this app is hardened beyond course scope. |
| Storage exceptions are not normalized at API boundary | [app/storage.py](../app/storage.py), [app/main.py](../app/main.py) | Valid | File or parse failures can bubble as uncontrolled server errors without a stable API response. | Add controlled error handling if this moves beyond the learning scope. |
| Local CORS/frontend base URL assumption | [app/main.py](../app/main.py), [frontend/index.html](../frontend/index.html) | Noise | This is real but mostly local-environment context; not a strong production issue for this project. | No code change needed for this submission. |

## Manual security check
I checked the repo state and runtime myself before accepting any evidence: `git branch --show-current` returned `final-project`, `./.venv/Scripts/python.exe -m pytest -q` returned `35 passed, 3 warnings in 0.51s`, and `Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/health` returned HTTP 200 OK. I also checked the Docker config and `.dockerignore` files to confirm the app was not being exposed with secrets or a dangerous runtime. This matters because it proves the evidence was based on actual execution and not on AI-generated claims alone.

## One AI output I rejected or corrected
I rejected the suggestion to treat Docker verification as fully proven without running the container. The repo had a valid Dockerfile and .dockerignore, but the runtime needed an actual health check. I corrected the wording to say only what we had verified: the container responded with HTTP 200, and the evidence is documented without over-claiming additional deployment coverage.

## Three AI usage rules
1. Never paste: I do not paste secrets, credentials, tokens, or local environment values into AI tools.
2. Always verify: I confirm commands, tests, and runtime behavior against the actual repo and a live check before I trust an AI result.
3. Record AI contributions by: noting which repo files were reviewed, what the AI suggested, what I accepted or changed, and what I rejected.

## Ownership statement
I am comfortable submitting this repo as my own work because I verified the branch state, the full pytest suite, and the live health checks before relying on any documentation claim. I reviewed the actual files that govern the repo rules, runtime behavior, and security posture instead of accepting generic AI output at face value. I corrected unsupported suggestions and kept the work within the intended course scope. I own the final decisions, and I can point to the specific evidence files and commands that support them.
