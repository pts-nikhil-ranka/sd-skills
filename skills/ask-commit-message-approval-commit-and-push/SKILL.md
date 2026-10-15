---
name: ask-commit-message-approval-commit-and-push
description: "Propose a concise Git commit message, get one explicit approval, commit only the agreed changes, verify the commit, and push it to origin. Use when the user wants an approval-gated commit-and-push workflow."
---

# Ask Commit Message Approval, Commit, and Push

Use this skill when the user asks to commit changes after approving the message and then push the resulting commit to the repository's `origin` remote.

## Workflow

1. Inspect before proposing.
   - Run `git status --short`, `git diff --stat`, and `git diff --check`; inspect enough of the diff to understand its scope.
   - Report the modified and untracked files that would be included. Preserve existing user changes; do not reset, checkout, amend, force-push, or include unrelated files without explicit scope.
   - If generated or unrelated files are present, call them out in the proposed scope.
   - Confirm that the repository has an `origin` remote and that the current branch is a named local branch. If either check fails, stop before proposing a mutation.
   - If there are no changes, do not create an empty commit unless the user explicitly requests one.

2. Propose and wait for approval.
   - Propose one concise commit message and a one-sentence scope summary.
   - Ask for one explicit approval of that exact message, scope, and the subsequent push to `origin`.
   - Do not stage, commit, or push before approval. Do not ask repeatedly unless the user changes the message or scope.
   - A response such as “go ahead” or “commit and push this” after the proposal counts as approval of the exact message, agreed files, and push to `origin`.

3. Commit only after approval.
   - Recheck `git status --short` because files may have changed while waiting.
   - Stage only the agreed paths. Stage all current changes only when the user explicitly approved the full current set.
   - Run `git add` followed by `git commit -m "<approved message>"`.
   - If Git write permission is blocked, request the necessary escalation and keep the approved message and scope unchanged.
   - If the commit fails for a non-permission reason, report the failure; do not silently change the message or scope or retry destructive alternatives.

4. Verify before pushing.
   - Run `git status --short`, `git log -1 --oneline --decorate`, and `git show --stat --summary HEAD`.
   - Push only if the commit succeeded, the worktree is clean, the current branch is still the agreed branch, and `origin` is still configured.
   - Push the current branch to the matching branch on `origin` without force, for example `git push origin HEAD:<current-branch>`.

5. Report the result.
   - Report the commit hash and message, the paths included, the push target, and whether the push succeeded.
   - If the push fails, report the failure without force-pushing or changing the approved commit.
