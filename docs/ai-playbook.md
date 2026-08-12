# Personal AI Coding Playbook

## 1. When I reach for AI first
- When I need a first draft of project documentation and I can verify every claim against the repo files.
- When I want a structured implementation plan before making a small, scoped project change.
- When I need to compare options for a design decision and then I will choose the simplest option that fits the current architecture.

## 2. When I do not reach for AI
- When the task would require secrets, credentials, tokens, or environment values.
- When the work is already clearly defined and small enough to do directly in the repo.
- When the change would add unsupported scope such as notifications, auth, or a production database.

## 3. My non-negotiables
- I only share the minimum context needed for the task.
- I treat assumptions as assumptions and clearly label them if they cannot be confirmed in the repo.
- I trace each claim back to a file, a test, or a live check before I treat it as evidence.
- I do not accept AI output as truth just because it sounds confident.

## 4. My review rules
- I check for over-claims before I accept an idea.
- I reject anything that broadens the project beyond its learning-project scope.
- I verify generated commands, code, and tests against the actual repo before I trust them.
- I keep notes of what AI suggested, what I accepted, what I changed, and what I rejected.

## 5. Course evidence that shaped these rules
- The project guardrails in [AGENTS.md](../AGENTS.md) explicitly say to keep changes small, read-only by default, and only change app files when explicitly approved.
- The AI prompt log in [prompt-log.md](prompt-log.md) shows the accepted pattern: propose, review, edit, and reject scope creep.
- The reflection and verification notes show that AI was useful for drafts and consistency, but human review was required for requirements, environment-specific commands, and final quality.

## 6. Ownership statement
I own the final decision for every AI-assisted change. I am responsible for checking the repo, validating the behavior, and rejecting anything that is unsupported, unverified, or outside scope. I will not paste secrets or sensitive data into AI tools, and I will not claim a result is correct unless I have a matching file, test, or runtime check.

## 7. Decision card
- For repo documentation: AI is useful as a draft generator, but I verify every fact against files.
- For code review: I use AI only as a second look, never as the final authority.
- For debugging: I verify the behavior with runtime checks and tests before trusting a fix.
- For architecture choices: I prefer the smallest option that fits the current app and course scope.
- I will never paste credentials, tokens, or sensitive environment values into an AI tool.
