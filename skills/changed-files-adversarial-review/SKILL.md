---
name: changed-files-adversarial-review
description: Adversarially review only the files, hunks, and behaviors changed for the current conversation or requested change set, then report only proven defects with material core impact. Use for reviews of current changes, a working-tree diff, patch, or changed files; use the repository-wide adversarial-review skill when the user asks to review the whole application.
---

# Changed Files Adversarial Review

Attack the assumptions and failure paths introduced or materially changed by the current conversation. Keep the review boundary narrow even when understanding the change requires reading surrounding repository code.

## Scope boundary

Establish the review set before judging defects:

1. Use the current conversation and active user goal to identify the files, generated artifacts, tests, documentation, and exact behaviors changed for this work.
2. Inspect `git status`, staged and unstaged diffs, and relevant untracked files as read-only evidence. Do not assume every dirty file belongs to this conversation; repositories may already contain unrelated user changes.
3. Prefer conversation-attributable hunks over whole-file scope. A changed file does not authorize reporting defects in untouched legacy code unless the scoped change newly exposes, depends on, or materially worsens them.
4. Read unchanged callers, dependencies, persistence code, recovery paths, documentation, and tests only as necessary to prove or disprove the impact of the scoped changes.
5. If attribution remains ambiguous, state the boundary and uncertainty. Ask the user only when the ambiguity would materially change the review.

Do not combine this with a repository-wide review unless the user explicitly asks to broaden the assignment. Do not report unrelated pre-existing defects discovered while tracing context.

## Review contract

- Reconstruct the promise of the change in plain language, including what is expected to remain unchanged.
- Map the affected state transitions from old behavior to new behavior: inputs, defaults, feature flags, ownership, external requests, confirmation, persistence, retries, exits, shutdown, migration, and restart.
- Challenge both configurations and transitions between them. A feature flag may be correct from a clean start but unsafe when changed while work is pending.
- Trace external effects end to end. Check whether the change can make local state disagree with broker, database, filesystem, network, or other external reality.
- Try to disprove candidates using existing guards, downstream reconciliation, tests, logs, and supported platform behavior.
- Review only unless the user separately asks for implementation. Do not edit code, create tickets, or mutate external systems because a defect was found.
- Preserve unrelated working-tree changes and treat production data as evidence, not permission to alter it.

## Core-impact gate

Report a finding only when all five elements are established:

1. **Changed promise:** A core capability or safety invariant affected by this change fails.
2. **Credible trigger:** A realistic input, transition, restart, timing window, or failure reaches it.
3. **Proven path:** The scoped diff and surrounding execution path demonstrate the failure. Separate static proof, test reproduction, and inference.
4. **Material consequence:** The result can cause plausible financial loss, security exposure, data corruption, unrecoverable state, serious incorrect behavior, or loss of a core workflow.
5. **Guard failure:** Existing validation, limits, retries, recovery, or tests do not prevent or contain it.

Reject style issues, naming preferences, generic hardening, speculative misuse, weak test-gap observations, and defects wholly independent of the scoped changes. Do not force a finding quota; no qualifying finding is a valid result.

## Adversarial method

1. Compare the intended before/after behavior and enumerate the change-owned entry points.
2. Trace normal flow once, then attack transitions and degraded states: partial success, ambiguous acknowledgement, timeout, retry, crash, stale persisted state, concurrent/manual intervention, configuration changes, rollback, and recovery after an external effect.
3. Check whether new branches bypass existing safeguards or reinterpret old durable states using incomplete status, identity, ownership, or version information.
4. Check backward and restart compatibility: old rows, old configuration, already-running work, submitted-but-unconfirmed effects, and generated artifacts consumed after deployment.
5. Verify survivors proportionately with targeted tests, read-only queries, logs, fixtures, or a concise deterministic scenario. Do not claim reproduction when evidence is only static.
6. Collapse symptoms into the smallest independent root causes and retain only the strongest one to three that pass the gate.

Pay particular attention when the change:

- adds a setting or feature flag but handles only clean startup rather than toggling during active work;
- treats a renamed or paused state as terminal even though an external request may still succeed;
- skips reconciliation, idempotency, persistence, or ownership checks on a newly added branch;
- changes a default without covering existing saved configurations or deployment artifacts;
- reports success before a durable acknowledgement or confirmation;
- blocks new effects but accidentally disables management, closure, rollback, or recovery of existing effects;
- adds a test that proves only the happy path while the implementation also claims restart or degraded-state safety.

## Findings

Lead with the verdict. Write each accepted finding in this order:

1. **Plain-language failure and impact:** Start with a specific, readable title and an opening paragraph that explains what can go wrong for the user or operator and why it matters. Do not mention code identifiers, setting names, internal states, functions, or file paths in this opening paragraph.
2. **Relatable example:** Give a short, concrete failure scenario.
3. **Technical cause and evidence:** Identify the change-owned promise that fails, the exact code and state path, the proof level, the material consequence, and why safeguards do not contain it. Put clickable file and line references here, not in the opening paragraph.
4. **Recommended correction:** Give the smallest safe remediation direction and the tests that would prove it.
5. **Severity:** End the finding with its severity and a brief justification.

State validation limits. If nothing passes the materiality gate, say that no deal-breaker was established and summarize the changed paths examined without turning uncertainty into a finding.
