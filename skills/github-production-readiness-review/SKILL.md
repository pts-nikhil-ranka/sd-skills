---
name: github-production-readiness-review
description: Review an existing codebase for production readiness and create concise, evidence-backed GitHub issues in its repository. Use when asked to review code after it is written and file issues for bugs, reliability gaps, safety concerns, test gaps, recovery flaws, or operational risks, with code permalinks, risks if unchanged, suggested solutions, and reusable labels.
---

# GitHub Production-Readiness Review

Review the codebase, then create actionable GitHub issues. Do not change application code unless the user separately asks for implementation.

## Workflow

1. Establish the repository, current branch/commit, review scope, and whether the user wants issues filed now. Treat an explicit request to use this skill for issue filing as permission to create the described GitHub issues and labels. Ask only if the repository or target is ambiguous.
2. Check GitHub authentication and repository access. Prefer an available GitHub connector; otherwise use the `gh` CLI. Stop and explain if authentication or write permission is unavailable.
3. Inspect the relevant source, tests, configuration, documentation, and recent changes. Use targeted searches first. Run read-only diagnostics and proportionate tests where available.
4. Fact-check claims that depend on current platform, broker, framework, security, or operational behaviour. Prefer official documentation, standards, primary sources, and reputable support documentation. Link sources directly in the issue.
5. Create an issue only for a distinct, evidenced finding. Create a `type: decision` issue when a missing business/risk decision prevents a safe technical recommendation.
6. Before filing, resolve a published commit SHA and verify it exists on GitHub. Use permanent code links in the form `https://github.com/OWNER/REPO/blob/SHA/path#Lx-Ly`. Never link a different remote revision as evidence for unpushed local code; ask the user to push it or state that a permanent link cannot yet be created.
7. Create the standard labels if absent. Do not overwrite an existing label's colour or description:
   - `priority: must-have`
   - `priority: important`
   - `type: code`
   - `type: testing`
   - `type: decision`
   - `status: review`
   - `codex: work next`
8. File each issue with the concise template below. Apply a priority and one type label. Create milestones/projects only when requested.
9. Verify each created issue: title, labels, sections, direct source link, and external references. Report URLs and confirm that no application code changed.

## Issue-writing rules

- Use plain, direct titles without tracking prefixes such as `EXE-01`.
- Begin every issue with a short plain-language paragraph explaining what can go wrong for the user or operator and why it matters. Do not mention code identifiers, setting names, internal states, functions, or file paths in this opening paragraph.
- After the opening paragraph, present information in this order: relatable example, technical cause and evidence, recommended correction, then severity.
- Keep each section crisp: bullets over long prose.
- State observed facts separately from the suggested solution.
- Include only the smallest useful code snippet (normally 3–12 lines). Put a clickable permanent link immediately above it.
- Explain the concrete production consequence in the opening paragraph and technical evidence; do not use generic warnings.
- Make the proposed solution an outcome and design direction, not a claim that it is already implemented.
- Include acceptance checks only when they materially make the issue actionable.
- Link official documentation only for factual claims that need it. Do not cite unsupported assumptions.
- Keep related but independently deliverable defects as separate issues. Cross-link dependencies when useful.

## Required issue template

```markdown
Plain-language explanation of the failure and its real-world impact, without code references.

## Example

- A short, concrete scenario showing how the failure affects a user or operator.

## Technical cause and evidence

- What the code does now, the proven execution path, why safeguards do not contain it, and the concrete risk if unchanged.

## Relevant code

[Short description](PERMANENT_GITHUB_CODE_LINK)

```language
// Small, directly relevant excerpt
```

## Recommended correction

- The safe implementation direction and intended result.

## Acceptance checks

- Observable conditions that prove the change works safely.

## References

- [Official source](URL)

## Severity

- Priority and a brief justification.
```

Omit `Example`, `Acceptance checks`, or `References` only when they add no value. Never omit the opening plain-language paragraph, `Technical cause and evidence`, `Relevant code`, `Recommended correction`, or `Severity`.

## Production-readiness focus

Prioritise findings that can cause incorrect execution, data loss/corruption, unsafe recovery, unauthorized scope, security exposure, uncontrolled cost, unavailable service, misleading observability, or untestable behaviour. For transaction/execution systems, distinguish request acceptance from confirmed execution; include partial, delayed, duplicate, timeout, reconnect, and restart paths.

## Completion

Return the issue URLs, the labels created/reused, the reviewed commit SHA, and a brief note on scope or unresolved decisions. Leave the repository worktree unchanged unless the user requested code changes.
