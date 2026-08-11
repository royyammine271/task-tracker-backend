# Personal AI Coding Playbook (Template)

## 1. When I reach for AI first
- When I need a first draft of repo documentation and I can verify every claim against files.
- When I want structured options for implementation plans before I change code.
- When I need help turning raw notes into decision logs, checklists, or comparison tables.

## 2. When I do not reach for AI
- When the prompt would require pasting secrets, tokens, credentials, or sensitive environment values.
- When I have not gathered enough repo evidence and would be guessing.
- When a change is small and I can apply it safely faster by direct edit.

## 3. My non-negotiables
- I only share the minimum context needed for the task and prefer generalized wording for internal findings.
- I treat unresolved ambiguity as a blocker and mark it explicitly instead of guessing.
- I keep outputs traceable: every technical claim should map to a file or to a clearly labeled assumption.

## 4. My review rules
- I check for over-claims first: anything not visible in files must be labeled as not visible.
- I validate risk language and ensure it does not minimize internal implementation exposure.
- I pick context strategy by task shape, then confirm the output stayed within that context boundary.

## 5. What I am still figuring out
- My exact threshold for switching from broad context (Strategy B) to narrow context (Strategy C).
- My default format for recording AI contribution evidence in each submission artifact.

## Decision Card
- For a new feature I reach for: Strategy B (structured context).
- For a code review I reach for: Strategy C (targeted context on anchor files).
- For debugging I reach for: Strategy C first, then Strategy B if cross-file behavior is unclear.
- For infrastructure I reach for: Strategy B with explicit assumptions called out.
- I will never paste secrets, credentials, tokens, or sensitive environment values into an AI tool.
- My one rule is: no unsupported claims; if I cannot verify it, I label it as not visible.
