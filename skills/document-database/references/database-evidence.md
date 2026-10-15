# Database discovery and evidence

Use a common documentation model while retaining native semantics. Relevant facts may come from schema definitions, migrations, generated schemas, read-only introspection, application queries, and tests. Record which source supports each claim. Tests establish tested scenarios; they do not alone establish deployment or all production behavior.

If sources disagree, identify the disagreement and the target being documented. A deployed database and a repository migration history can both be valid snapshots at different versions. Never merge incompatible snapshots into one supposedly verified schema.

## Common representation

For each database object, retain engine/database/namespace/name, object kind, purpose, structure, constraints, relationships, related behavior, and evidence. Qualify names to avoid collisions. Preserve native types and expressions verbatim alongside their plain-language explanations. Use “not applicable” only when established, and “unknown/not inspected” when evidence is missing.

Application flows are independent of schema extraction: trace entry points through services/repositories/raw SQL and into stored routines, triggers, and jobs. Account for dynamic query paths where discoverable and describe search limitations. Do not imply that a foreign key proves a user-visible feature or that the absence of a foreign key proves the absence of a relationship.

## SQLite

Use the existing driver/tool with a read-only connection or an appropriate snapshot. Inspect `sqlite_schema` definitions plus supported metadata interfaces such as `table_xinfo`, `foreign_key_list`, `index_list`, and `index_xinfo`. Verify availability against the actual SQLite version. Quote identifiers safely or use supported table-valued PRAGMA interfaces with parameters; do not interpolate unchecked identifiers.

`table_xinfo` includes generated/hidden columns omitted by `table_info`. Preserve declared type and explain affinity/STRICT mode where relevant. Examine original DDL for checks, generated expressions, partial/expression indexes, virtual tables, and WITHOUT ROWID. Do not assume every integer-like primary key has identical rowid behavior or that all primary key forms imply the same nullability.

Distinguish declared foreign keys from enforcement in the application's connections. A read-only inspection connection's `foreign_keys` value does not prove the application's connection setting. Inspect connection initialization when available. Document uncertainty instead of changing PRAGMA settings.

References: https://www.sqlite.org/pragma.html and https://www.sqlite.org/foreignkeys.html

## PostgreSQL

Use the project's existing connection tools with read-only queries. Standard metadata in `information_schema` is a starting point; PostgreSQL catalogs and supported definition functions provide engine-specific detail. Verify queries against the actual server version and permissions. Metadata visible to one role may be incomplete; record that limitation.

Inspect relevant schemas, tables, columns, defaults, constraints, and indexes. Include native details when present: enum/domain types, identity/sequences, generated columns, expression/partial indexes, included columns, partitions, views/materialized views, triggers, routines, and row-level security policies. Avoid assuming `information_schema` exposes every relevant feature.

Separate database permissions and row policies from application authorization checks. Schema-level uniqueness and foreign keys do not prove tenant isolation. Record enforcement from the relevant evidence rather than inferring it from naming.

References: https://www.postgresql.org/docs/current/information-schema.html and https://www.postgresql.org/docs/current/catalogs.html

## Other engines

Apply the same representation and evidence rules. First inspect the project's existing schema tooling and consult authoritative documentation for engine/version-specific introspection. Adapt only extraction and native explanations; retain the table/action/flow reading experience. If an engine lacks tables, keys, transactions, or indexes in the relational sense, describe its actual collection/document/relationship model and mark non-applicable concepts explicitly. Do not claim universal tested compatibility from the SQLite and PostgreSQL guidance.
