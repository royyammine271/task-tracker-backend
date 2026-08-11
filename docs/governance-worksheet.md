# Module 5 Governance Worksheet

Source used for items: security findings currently documented in docs/security-review.md.

| Item shared | Risk | Reason | Safer future version | Ambiguity to resolve |
|---|---|---|---|---|
| S-01 Unbounded user text fields | Medium | This shares internal validation gaps in application behavior, which is non-sensitive but still implementation detail. | In a sample FastAPI app, some user-input fields are length-checked inconsistently; suggest generic validation patterns without seeing exact schema. | Is the repository public or private? If public course repo, this could be Low. |
| S-02 No auth/authorization outside course scope | Medium | This discloses a known control absence in a specific codebase, which is internal security posture information. | In a classroom toy app with no real users, auth is intentionally omitted; provide a checklist for adding auth in production. | Was any deployment URL or environment detail shared with this finding? |
| S-03 Storage I/O and JSON parse exceptions can bubble as server errors | Medium | This exposes concrete failure-mode details of backend persistence and error handling. | A local file-backed API may surface unhandled storage exceptions; suggest generic exception-boundary patterns. | Were stack traces, filesystem paths, or runtime logs shared, or only high-level description? |
| S-04 Local CORS/frontend base URL assumption | Medium | This reveals environment/config assumptions about allowed origins and frontend wiring, which are internal setup details. | For local dev CORS, review principle-based origin allowlisting patterns without project-specific hostnames. | Were exact hostnames/ports and deployment targets shared beyond localhost? |
| S-05 Unpinned dependencies / CI drift risk | Medium | This reveals dependency-management and CI hardening posture, which is operational implementation context. | In a Python CI pipeline, dependencies are not fully pinned; recommend reproducible install strategy and lockfile approach. | Did you share full dependency lists and workflow files, or only the risk statement? |
| S-06 CI lacks security scan steps | Medium | This communicates specific control coverage gaps in your pipeline even if no secrets are included. | A course CI currently runs tests only; suggest optional baseline SAST/dependency-scan additions for production-like setups. | Is this repo only educational and non-deployed, or used beyond coursework? |

## Notes

- This worksheet avoids guessing beyond what is currently documented.
- If you add a true "What I Shared" table later, this file should be updated to classify those exact rows instead.
