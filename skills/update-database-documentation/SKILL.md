---
name: update-database-documentation
description: Update database documentation whenever database design or schema changes, including adding, removing, or modifying columns or tables. Use when making schema changes or synchronizing documentation with an existing schema change.
---

# Update Database Documentation

For every change to the database design or schema, update the relevant database documentation as part of the same change. This includes adding, removing, or modifying columns or tables.

Inspect the affected schema definitions, migrations, and existing database documentation to identify what changed. Follow the project's existing documentation structure and conventions; if no relevant documentation exists, create a focused database document in the project's documentation location.

Document the resulting structure accurately, including affected column types, nullability, defaults, keys, constraints, indexes, and relationships where applicable. Remove or revise obsolete descriptions of deleted or renamed objects, and update affected schema diagrams and examples when present.

Verify the documentation against the resulting schema and migrations. Keep the work scoped to the database changes; do not alter the schema merely to match stale documentation. Report which documentation files were updated and any unresolved discrepancies.
