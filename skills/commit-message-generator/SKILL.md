---
name: commit-message-generator
description: "Generate a concise, evidence-backed Git commit message from the current diff without staging, committing, amending, or pushing."
---

# Commit Message Generator

Use this skill when the user asks for a commit message, commit title, or concise summary of changes based on the current Git worktree.

## Workflow

1. Inspect read-only Git state with `git status --short`, `git diff --stat`, `git diff --check`, and the relevant diff. Check recent `git log --oneline` to match the repository's existing message style.
2. Separate coherent requested changes from unrelated, generated, temporary, or user-owned files. Call out those files explicitly instead of silently including them.
3. Propose one concise message grounded in the diff. Prefer the repository's established style; otherwise use a conventional-commit shape such as `fix: align hedge targets with two-leg cycles`.
4. Give a one-sentence scope summary and, when useful, list the paths the proposed commit would include. Mention validation evidence such as `git diff --check` without claiming tests or compilation that were not run.

## Boundaries

- This skill drafts a message only. Never stage, commit, amend, reset, checkout, push, or otherwise mutate Git state.
- Do not invent behavior, tests, issue numbers, or file scope not supported by the diff.
- If the worktree is clean, say there are no changes to describe rather than suggesting an empty commit.
- If changes are mixed, provide a message for the coherent requested subset and identify the unrelated/generated files that should remain outside the commit.
- Keep the output compact unless the user requests a detailed commit body or multiple alternatives.
