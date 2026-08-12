# Personal AI Coding Playbook

## 1. When I reach for AI first
- I use AI to draft project docs, release notes, and summaries when I can verify every claim against the repo before I keep it.
- I ask AI for a first pass on a task plan when the task is small, scoped, and clearly tied to a file or workflow already in the project.
- I use it to compare options for a design decision, then choose the smallest option that fits the current architecture instead of accepting the biggest idea.
- It was especially useful for turning repo facts into clean structure: README checks, release evidence, and review summaries.

## 2. When I do not reach for AI first
- I do not use AI for anything involving secrets, credentials, tokens, or environment values.
- I do not let AI drive the work when the task is already obvious and I can do it directly in the repo without guesswork.
- I slow down when the task would add unsupported scope, such as auth, production storage, notifications, or feature creep that is not in the project.
- I also avoid using it as the final authority when a decision depends on a real runtime check or the repo’s actual branch/test state.

## 3. My non-negotiables
- I only share the minimum context required for the task.
- I treat assumptions as assumptions and label them as such until they are confirmed by code, tests, or a live check.
- I trace each claim back to a file, a command, a test run, or a runtime result before I trust it.
- I do not accept AI output just because it sounds confident, and I do not paste personal or sensitive data into AI tools.
- I own the final decision and the final wording in any repo artifact I submit.

## 4. My review rules
- I check for over-claims before I accept an idea.
- I inspect the diff and ask: does this match the project scope, the guardrails, and the actual repo state?
- I verify generated commands and documentation with real commands and real outputs, not with guesses.
- I grade findings by usefulness, not by how polished the sentence sounds; if the conclusion is shallow or unverified, I reject it.
- I keep a record of what AI suggested, what I accepted, what I corrected, and what I rejected.

## 5. What I am still figuring out
- I am still learning when AI is most useful for code review versus when it becomes a distraction.
- I want better team norms for deciding when a suggestion is a real fix versus a broad “good idea” that should be downgraded or refused.
- I am still refining how much repo context to give the tool without creating false confidence or overfitting to a narrow example.

## 6. Decision Card
- New feature: AI can help draft the plan, but I still decide whether it matches the project’s scope and rules.
- Code review: AI is a second look, not the final authority.
- Debugging: I verify behavior with real commands and tests before trusting a fix.
- Infrastructure: I look for explicit runtime evidence and avoid over-claiming on Docker, CI, or deployment conditions.
- Never-paste: I will not share secrets, credentials, tokens, or environment values with AI.
- One rule: if I cannot show evidence from the repo or a live check, I do not keep the claim.
