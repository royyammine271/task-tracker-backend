# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| Update the local run command to show the exact Windows PowerShell flow and verified results. | Useful | This was actionable and matched the repo state; it prevented stale or vague instructions. | Kept and tied to the actual verified commands. |
| Add a clear Docker command block that matches the actual runtime evidence. | Useful | It reduced ambiguity and tied the docs to a real container run instead of a theoretical example. | Kept and aligned with the Docker health check. |
| State the health endpoint result without claiming Docker succeeded unless runtime was checked. | Useful | This prevented an over-claim and kept the evidence honest. | Kept; this correction was necessary before final handoff. |
| Rewrite the final readiness notes to be shorter and explicit about warnings vs failures. | Noise | This mostly improved wording and did not materially change technical risks or repo behavior. | Accepted only as wording cleanup, not a technical fix. |

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
