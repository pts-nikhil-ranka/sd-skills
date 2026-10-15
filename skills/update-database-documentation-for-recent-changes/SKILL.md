---
name: update-database-documentation-for-recent-changes
description: Update database documentation only for database changes implemented in the latest or recent conversation. Use for requests to document recent conversational changes rather than reconcile the entire database schema or historical documentation drift.
---

# Update Database Documentation for Recent Changes

Update database documentation only for database design or schema changes actually implemented in the latest or recent conversation. This includes additions, removals, or modifications to tables, columns, and related schema objects. Do not perform a repository-wide documentation reconciliation.

## Establish the change scope

Use the available conversation history to identify the most recent implemented database change set, including related follow-up edits. Follow any explicit conversation, commit, or change range specified by the user. Exclude proposed but unimplemented work and changes subsequently reverted.

Confirm the scoped changes against the relevant diffs, migrations, and schema definitions. A change may already be committed; do not assume the working-tree diff contains every conversational change. Conversely, do not treat every uncommitted change or the latest commit as part of the conversation without supporting evidence.

If the relevant conversation or change scope is unavailable or ambiguous, ask the user to identify it before editing documentation. If the conversation contains no implemented database changes, report that no documentation update is needed.

## Update only affected documentation

Find the existing database documentation and follow its structure and conventions. Update only sections, diagrams, and examples affected by the scoped changes, including directly affected references to renamed or removed objects. If no suitable document exists, create a focused document in the project's documentation location that describes only the scoped changes and the context needed to understand them.

Describe the resulting schema accurately, including affected types, nullability, defaults, keys, constraints, indexes, and relationships where applicable. Read surrounding schema for context without expanding the edit scope to unrelated tables, historical changes, or pre-existing documentation gaps. Do not modify database code or migrations as part of this documentation task.

Verify every documentation edit against the implemented changes and resulting schema. Review the final diff to ensure each edit is attributable to the selected conversational change set. Summarize the database changes covered and the documentation files updated; identify any unresolved ambiguity without guessing.
