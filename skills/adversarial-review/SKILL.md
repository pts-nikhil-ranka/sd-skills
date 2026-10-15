---
name: adversarial-review
description: Adversarially review an existing application by attacking its assumptions and failure paths, then report only proven defects that materially threaten core user outcomes, safety, financial or data integrity, or operational continuity. Use for offensive, adversarial, deal-breaker, critical-risk, or production-failure reviews; do not use for broad linting, style feedback, exhaustive bug lists, or filing issues in an external tracker.
---

# Adversarial Review

Act as an offensive reviewer: understand what the application promises, then actively search for realistic ways its assumptions, state transitions, safeguards, and recovery can fail. After discovery, apply a core-impact gate so only consequential findings survive. Issue count is not a success metric. A review with no qualifying finding is better than one padded with weak observations.

## Two phases

1. **Adversarial discovery:** Generate and investigate failure paths aggressively. Challenge normal-flow assumptions, external dependencies, degraded states, and recovery behavior without limiting discovery to an issue quota.
2. **Impact qualification:** Report only the smallest set of independent root causes that pass the core-impact gate. Do not confuse discovering many candidates with producing a valuable review.

## Review contract

- Reconstruct the application's core promises and execution model before judging defects. Read the relevant documentation, entry points, state transitions, tests, persistence, and external-effect boundaries.
- Prioritize supported, realistic operating conditions. A documented limitation can still qualify when the application fails open, cannot enforce the limitation, or exposes ordinary users to severe harm.
- Think offensively about failures: partial success, retries, timeouts, crashes, stale state, concurrency, ownership confusion, boundary values, resource exhaustion, invalid external responses, and recovery after an effect has already occurred.
- Review only unless the user also asks for changes. Do not edit code, create tickets, send messages, or mutate external systems merely because a defect was found.
- Preserve unrelated user changes and treat production data as evidence, not as permission to alter it.

## Core-impact gate

Report a finding only when all of these are present:

1. **Core capability:** Identify the application promise or safety invariant that fails.
2. **Credible trigger:** Describe a realistic event, input, sequence, or operating condition that reaches the failure.
3. **Proven path:** Trace the relevant code and state transitions. Distinguish observed facts from inference.
4. **Material consequence:** Show plausible financial loss, security exposure, data corruption, unrecoverable state, serious incorrect behavior, or loss of a core workflow.
5. **Guard failure:** Explain why existing validation, limits, retries, tests, or recovery do not prevent or contain it.

Reject or demote candidates that are primarily style, naming, generic hardening, speculative misuse, minor UX, duplicate manifestations of one root cause, or test gaps without a demonstrated product risk.

Do not force a finding quota. By default, return only the strongest one to three independent root causes. Return fewer when evidence does not justify more.

## Method

1. State the product's goal in plain language, including what causes external effects and how success or failure is decided.
2. Map the critical state machine: inputs, ownership, calculations, external requests, confirmations, persistence, retries, exits, shutdown, and restart.
3. Trace capital-, safety-, security-, or data-risking paths end to end. Check whether local state can disagree with external reality.
4. Generate candidate failure paths, then try to disprove them using guards, downstream reconciliation, tests, logs, and platform behavior.
5. Validate the survivors proportionately: targeted tests, read-only queries, logs, fixtures, or a concise deterministic scenario. Do not claim reproduction when evidence is only static.
6. Rank by consequence, likelihood, blast radius, detectability, and recoverability. Prefer one root cause over several symptoms.

Pay special attention to:

- an external effect succeeding while local persistence or acknowledgement fails;
- a partial result being treated as complete, or blocking all recovery indefinitely;
- retries that can duplicate irreversible effects;
- risk controls that activate too late, inspect the wrong scope, or disappear during degraded states;
- broad ownership selectors that can include another user's, tenant's, account's, or workflow's resources;
- fail-open behavior when prerequisites are absent;
- restarts that reconstruct from ambiguous, stale, or differently scoped state;
- locks or idempotency mechanisms whose scope is narrower than the external system;
- emergency, rollback, or close paths that depend on the same component that has failed.

## Finding standard

Lead with the verdict. Write each accepted finding in this order:

1. **Plain-language failure and impact:** Start with a specific, readable title and an opening paragraph that explains what can go wrong for the user or operator and why it matters. Do not mention code identifiers, setting names, internal states, functions, or file paths in this opening paragraph.
2. **Relatable example:** Give a short, concrete scenario with values where useful.
3. **Technical cause and evidence:** Identify the affected core promise, exact code/state path, proof level, consequence, and why current safeguards do not contain the failure. Put clickable file and line references here, not in the opening paragraph.
4. **Recommended correction:** Give the smallest safe remediation direction and the tests that would prove it.
5. **Severity:** End the finding with its severity and a brief justification.

Use clickable file and line references when available. Separate confirmed production evidence, test reproduction, and static proof. State important validation limits.

If no candidate passes the materiality gate, say that no deal-breaker was established. Summarize what was examined and any important uncertainty without converting it into a finding.
