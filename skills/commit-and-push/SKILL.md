---
name: commit-and-push
description: "Inspect Git changes, update the changelog when applicable, generate a concise commit message, commit the intended scope without a commit-message approval pause, verify the commit, tag the release when applicable, and push the current branch and applicable tag to origin. Use when the user asks to commit and push without requesting an approval-gated workflow."
---

# Commit and Push

Use this skill when the user has asked to commit changes and push the resulting commit. That request authorizes the clear, requested Git scope, applicable release tagging under repository conventions, and a normal push of the branch and applicable release tag to `origin`; it does not authorize unrelated files, amending, bypassing hooks, resetting, or force-pushing.

## Workflow

1. Inspect the repository before mutating it.
   - Run `git status --short`, `git diff --stat`, and `git diff --check`, inspect the relevant diff, and check recent `git log --oneline` entries for the repository's message style.
   - Identify the requested change set separately from unrelated, generated, temporary, or user-owned changes. Preserve excluded changes.
   - If the intended file scope is materially ambiguous, stop and ask about scope. This is distinct from commit-message approval.
   - Confirm that `origin` exists and that the current branch is a named local branch. Stop if either condition fails.
   - Inspect repository release instructions, version metadata, existing tags, and release tooling to determine whether this change set represents a release that requires a tag. An existing tag history alone does not mean every commit should be tagged. Derive the exact release version and tag name from repository conventions or an explicit user instruction; if a required version cannot be determined, ask rather than inventing one.
   - If there are no changes, do not create an empty commit unless the user explicitly requested one.

2. Update the changelog when applicable, before committing.
   - Inspect repository instructions, release documentation, existing changelog entries, and relevant tooling to determine whether the intended changes require a changelog update.
   - When applicable, add or update a concise, evidence-backed entry describing only the intended changes. Follow the repository's format, categories, and unreleased or version/date conventions; do not invent a release version or date. Preserve unrelated entries and avoid duplicating an entry that already covers the changes.
   - If release tooling generates the changelog, follow the repository's established workflow, updating source entries or release fragments when required rather than manually editing generated output. Do not publish a release as part of this step.
   - If the repository has no changelog practice or the intended changes are exempt under its conventions, skip the update. Do not introduce a changelog unless repository instructions require one.
   - For an applicable release, ensure any required version metadata and changelog entries agree with the intended release version before committing. Include those updates and any applicable changelog or source-entry changes in the same commit as the intended changes. Review the resulting diff and run `git diff --check` before selecting the message and staging.

3. Select the commit automatically.
   - Generate one concise, evidence-backed commit message that matches the repository's established style; otherwise use a clear conventional-commit message.
   - Do not ask the user to approve the message. A brief commentary update may state the chosen message and scope, but must not pause execution.

4. Commit only the intended changes.
   - Recheck `git status --short` immediately before staging because the worktree may have changed during inspection.
   - Stage explicit intended paths. Use `git add -A` only when the user clearly requested all current changes.
   - Run `git commit -m "<selected message>"` without `--amend` or `--no-verify`.
   - If Git write permission is blocked, request the necessary escalation without changing the selected scope or message.
   - If staging, hooks, or the commit fail for another reason, report the failure and stop; do not bypass safeguards or use destructive recovery.

5. Verify the commit.
   - Run `git status --short`, `git log -1 --oneline --decorate`, and `git show --stat --summary HEAD`.
   - Confirm that the created commit contains the intended paths, including any required changelog, source-entry, or release metadata updates, the branch has not changed, `origin` is still configured, and any remaining worktree changes are known exclusions rather than unexpected mutations.

6. Tag the release after committing, when applicable.
   - If this change set does not require a release tag under the repository's conventions, skip tagging and state why.
   - When a tag is required, check for the exact tag name both locally and on `origin`. If it already exists, verify that it resolves to the verified commit before reusing it. Stop and report any conflicting target; never move, delete, overwrite, or force-push an existing tag.
   - Create the tag at the verified commit hash, following the repository's tag naming and annotated, lightweight, or signed-tag conventions. Verify that the tag resolves to that commit before pushing. If tag creation or signing fails, report the failure and stop without bypassing the required convention.
   - If established release automation owns tag creation, use its documented workflow instead of creating a competing tag manually. Verify the resulting tag after the workflow runs; if it is still pending, report that state explicitly.

7. Push and verify the remote result.
   - Push without force using `git push origin HEAD:<current-branch>`.
   - If a release tag was created or reused locally, push only that tag with `git push origin refs/tags/<release-tag>:refs/tags/<release-tag>`. Do not use `--tags` or otherwise push unrelated tags.
   - Confirm that the remote branch and applicable release tag resolve to the verified commit. For an annotated tag, check the commit it points to, not just the tag object.
   - If either push fails, report which refs succeeded and which failed, then stop without force-pushing, rewriting the commit, or changing the destination. Preserve the local commit and tag for recovery.

8. Report the result.
   - Provide the commit hash and message, included paths or a concise scope summary, the push target, push outcome, changelog update or reason for skipping it, release tag and its push or automation outcome (or reason for skipping tagging), and any intentionally uncommitted changes.
