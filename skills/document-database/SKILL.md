---
name: document-database
description: Create or improve an engineer-facing HTML database guide that connects tables, columns, keys, indexes, and relationships to verified application use cases and data-flow diagrams. Use for database onboarding guides, visual schema documentation, and table-to-action maps across database engines, including SQLite and PostgreSQL. Do not use for a narrow schema-change documentation update unless this guide is explicitly requested.
---

# Document Database

Create a database-first HTML guide. An engineer starts with a table, understands what its rows mean, and sees every verified action that reads or changes it. Shared application use cases are linked supporting modules. Use Mermaid for diagrams and Tailwind CSS for styling. The delivered guide is HTML, even though this skill's instructions are Markdown.

## Establish the evidence

Inspect existing documentation, database tools, schema definitions, migrations, and application entry points before choosing an extraction approach. Reuse the project's tools when they support the task. Do not add a database framework just to write documentation.

Identify the engines, databases/namespaces, relevant code revision, schema source, and requested scope. Default to every application-owned table in the selected application. Account for join tables, history/audit tables, background-job tables, and framework-managed tables; group them when appropriate. Explicitly list excluded databases, namespaces, or objects. Never silently truncate a large schema.

Use schema files and application source when available. Read live metadata only through an authorized connection using read-only operations. Do not run migrations, change database settings, or query customer rows merely to document structure. Use repository-backed actions for documentation and review examples. Use synthetic values only when illustrating data, label them, and never infer application behavior from them. Keep credentials and connection secrets out of artifacts.

Read [references/database-evidence.md](references/database-evidence.md) for engine-specific discovery and evidence rules. Database agnosticism means a shared documentation format with engine-aware extraction; it does not mean pretending all engines enforce the same rules.

## Shared use cases and token-efficient maintenance

Use cases belong to application documentation and must be independently readable. The database guide references them; it does not own or duplicate their workflow descriptions. Inspect existing use-case documentation first and reuse its canonical source and stable identifiers. Do not create parallel descriptions of the same workflow.

Read [references/shared-use-cases.md](references/shared-use-cases.md) when creating or updating flows or their database mappings. Maintain one source per use case, with business steps and optional database details attached to those steps. Use standard JSON for new structured source files. Generate the business view, optional database layer, plain-language explanations, and reverse table/action mappings from these shared sources. Each standalone HTML flow has a “Show database details” button; the database guide can link directly to its expanded state.

Keep schema definitions in the database catalog and reference objects by stable IDs. Derive table-to-action mappings from the shared use-case sources instead of maintaining a second mapping by hand. For incremental work, inspect the compact index and load only affected use cases and schema entries, expanding to related dependencies when needed. Hiding details in the UI alone does not save authoring tokens; avoid repeated source descriptions and unnecessary whole-guide regeneration.

## Connect structure to behavior

Build an inventory of tables and trace application actions from user interfaces, APIs, services, queries, stored routines, and background jobs. Trace both directions: action to database objects, and each table back to its readers and writers. Explain indirect support through joins, views, triggers, cascades, and asynchronous work.

Do not generate create/read/update/delete actions from a table name alone. For each action, record the actor, trigger, purpose, preconditions, ordered reads/writes, participating objects, affected fields when known, transaction boundaries, and outcome. Include authorization or tenant restrictions when they affect which data can be accessed. Describe implemented failure behavior, especially partial work across separate transactions or asynchronous steps. Mark anything not established as unknown.

Distinguish physical deletion from deactivation, archival, and soft deletion. Distinguish database-enforced relationships from relationships maintained only by application code. A UI action can touch many tables; a table can serve many actions. Preserve these many-to-many mappings.

Attach source evidence to schema facts and action mappings. Use repository-relative paths with symbols/line locations and revision metadata, or metadata-query provenance. Prefer revision-specific repository links when available. Identify code-derived expectations separately from observed database state. Do not claim deployment or runtime verification from source inspection.

If a table has no discovered caller, label it “No caller found in inspected scope,” with the search scope. Do not call it unused. If application source is missing, deliver the schema view and explicitly mark action mappings unverified rather than inventing them.

## Produce the guide

Read [references/html-format.md](references/html-format.md) before generating or changing the guide. It defines the reviewed layout, narrative style, diagram semantics, dot navigation, table modals, and acceptance checks. Reuse or adapt [assets/guide.css](assets/guide.css) to preserve the reviewed visual style; keep application facts in source data rather than in presentation code.

Use one table per HTML file. The catalog index is a short directory of links, not a page containing multiple table definitions. Each table page has structure on the left and all verified supported actions on the right. Lead with a practical question the table answers, explain what one row represents, and explain how to interpret its data. Link related tables to their own pages. For an individual use case, lead with a short business paragraph and the workflow, then provide explanatory outcomes, table details, and maintenance/evidence sections. Link each action to its independently readable shared use-case page, with database details enabled. Do not copy the flow into the database guide. Keep a relationship overview as supporting context. Split complicated flows into connected numbered stages with local branches instead of a tangled chart. Preserve unchanged stages when revealing database details.

Use exact catalog names in table nodes. Clicking a table node opens its details in an accessible modal that shares the catalog data. Show alternating row shading in schema tables. Reuse the matching dot-navigation markup, CSS and JavaScript described in the HTML reference; do not combine replacement dot markup with existing rail styles. Keep its dot group centered on the visible viewport, with section names on hover/focus and usable touch controls. Add “What this means in practice” for business consequences and failure paths rather than another list of diagram nodes.

Respect an established documentation destination. Otherwise use `docs/database/index.html` for the table directory, `docs/database/tables/<table-id>.html` with a matching JSON source for each table, and `docs/use-cases/` for shared use-case sources and standalone HTML pages, with any necessary local assets. Preserve unrelated existing documentation. Record schema coverage, evidence gaps, extraction date/time with timezone, and version/revision if known. Update a project changelog when its instructions require it.

When the user asks to iterate on the format before updating a skill, build and refine a review example first. Do not treat an unaccepted proposal as the final format or update the skill until requested. Prefer a traced action from the selected repository over a hypothetical scenario. Do not document an unrelated current project merely because it is the working directory.

## Verify and deliver

Reconcile the guide against the complete in-scope inventory. Verify primary and foreign keys, composite key order, indexes, defaults, nullability, relationships, and engine-specific facts. Check that each table has evidence-backed action mappings or an explicit evidence gap. Check both directions of every derived mapping and all cross-links. Verify that both flow views come from the same source and that business steps, decisions, and outcomes remain consistent when database details are toggled.

Parse and render every Mermaid diagram with the selected version. Inspect the actual HTML in a dedicated new browser window when browser testing is available. Check the viewport-centered dot navigation, staged flow layouts, exact table labels, database-details toggle, table modals, direct-link state, alternating table rows, narrow layout, print output, and long names. Verify pointer, keyboard, and touch behavior where available. Do not reuse the user's browser window. If rendering or browser validation is unavailable, state exactly what remains unchecked rather than claiming visual verification.

Report the output location, covered databases and objects, evidence limitations, and checks actually performed. For a skill-only request, deliver the skill itself and distinguish skill validation from testing generated documentation against a real application.
