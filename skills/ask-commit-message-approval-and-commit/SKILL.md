---
name: ask-commit-message-approval-and-commit
description: "Propose a concise Git commit message, get one explicit approval, commit only the agreed changes, and verify the result. Use when the user wants a commit-message approval gate without an automatic push."
---

# Ask Commit Message Approval and Commit

Use this skill when the user asks to commit Git changes and wants to approve the commit message once before the repository is mutated.

## Workflow

1. Inspect before proposing.
   - Run `git status --short`, `git diff --stat`, and `git diff --check`; inspect enough of the diff to understand its scope.
   - Report the modified and untracked files that would be included. Preserve existing user changes; do not reset, checkout, amend, push, or include unrelated files without explicit scope.
   - If generated or unrelated files are present, call them out in the proposed scope.
   - If there are no changes, do not create an empty commit unless the user explicitly requests one.

2. Propose and wait for approval.
   - Propose one concise commit message based on the diff, along with a one-sentence scope summary.
   - Ask for one explicit approval of that exact message and scope.
   - Do not stage or commit before approval. Do not ask repeatedly unless the user changes the message or scope.
   - A response such as “go ahead” or “commit this” after the proposal counts as approval of the exact message and agreed files.

3. Commit only after approval.
   - Recheck `git status --short` because files may have changed while waiting.
   - Stage only the agreed paths. Stage all current changes only when the user explicitly approved the full current set.
   - Run `git add` followed by `git commit -m "<approved message>"`.
   - Never amend an existing commit, force-push, push, or alter files unless separately requested.
   - If Git write permission is blocked, request the necessary escalation and keep the approved message and scope unchanged.
   - If the commit fails for a non-permission reason, report the failure; do not silently change the message or scope or retry destructive alternatives.

4. Verify and report.
   - Run `git status --short`, `git log -1 --oneline --decorate`, and `git show --stat --summary HEAD`.
   - Report the commit hash and message, the paths included, and whether the worktree is clean.
