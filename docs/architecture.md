# Architecture Strategy Comparison Log

## 1. Strategy comparison table

| Strategy | What it got right | What it got wrong, missed, or invented | Best suited task shape |
|---|---|---|---|
| Strategy A (minimal context) | Produced a complete one-page architecture with all required sections, included backend and frontend flow in the create-task path, and listed practical key files across API, models, storage, tests, and docs. | It includes broad cross-repo claims (for example local/CI convention references and intent-level assumptions about comment shape) without a structured provenance frame in the draft itself, so review traceability is weaker than B. | Fast turnaround architecture drafts when you want broad coverage and can tolerate follow-up fact-checking. |
| Strategy B (structured context) | Kept the same useful breadth as A, but with clearer structure and guardrails from AGENTS.md plus file summaries; it stayed concise, section-complete, and explicit about assumptions. | Still carries one assumption-level statement about comments being intentionally string-based; also pulls AGENTS.md into key files, which is useful for governance context but not strictly runtime architecture. | Best for production-quality course documentation where you need both breadth and controlled context with fewer blind spots. |
| Strategy C (targeted anchor files) | Strongest factual discipline: it explicitly marks uncertainty as "not visible from the files I read," avoids overreach, and gives a clean API/model/storage-centered architecture. | Misses frontend behavior, test conventions, and some cross-file business-rule details by design; key-files section is thinner and less representative of whole-repo architecture. | Best for narrow, high-confidence backend summaries or audit-style writeups where over-inference risk must be minimized. |

## 2. Verdict

I chose Strategy B for the final architecture document because it preserves the broad architectural coverage seen in A while giving better context control and clearer justification boundaries than A, and far fewer intentional blind spots than C. In these drafts, B is the best balance between completeness and reliability: it captures end-to-end app architecture (API, models, storage, frontend, tests, conventions) without the large omission surface that comes with a strictly targeted read.

## 3. Two-sentence context-engineering rule

For task shape "one-page architecture summary that must represent the whole app," I use strategy B because structured context gives enough breadth to cover backend, frontend, storage, and conventions while still constraining drift. For task shape "precision-first subsystem summary with strict evidence boundaries," I use strategy C because anchored files force explicit uncertainty marking instead of accidental inference.
