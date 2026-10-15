# Shared use cases with optional database details

## Ownership and reuse

A use case is application documentation. It must explain the action without requiring the reader to open the database guide. Keep database schema facts in the catalog and workflow facts in a single canonical use-case source. Other documentation links to that use case by stable ID.

First inspect the project's existing documentation format and renderer. Extend them when they can represent business steps and attached database operations. Do not introduce a second source of truth or convert unrelated documentation. Use widely adopted file formats. For new structured documentation, use standard, readable JSON: a compact file per use case, a file per table definition, and a small derived index. Preserve an established suitable source format rather than introducing duplicate authoritative files. JSON is the editable source and HTML is the reader-facing output. Default paths are `docs/use-cases/<id>.json`, `docs/use-cases/<id>.html`, and `docs/use-cases/index.json`; table definitions default to `docs/database/tables/<id>.json`, and table HTML pages default to `docs/database/tables/<id>.html`. The directory is `docs/database/index.html`. Each table has its own JSON source and HTML page, including review examples. The database index links to those pages; it does not combine their schemas.

One authoritative source does not prohibit two generated SVGs. The important constraint is that the business sequence, database annotations, and reverse mappings are authored once. Generated artifacts are reproducible and must not be hand-edited independently.

## Minimal source contract

Adapt field names to established project conventions. With a new JSON format, retain:

- Use-case ID, title, purpose, a short business summary paragraph, actor, trigger, preconditions, outcomes, evidence, and source revision.
- Business steps with stable IDs, concise diagram labels, explanatory descriptions, optional business headings, and explicit directed transitions. Transitions name branches and asynchronous boundaries. Include business-visible failure paths in this layer.
- Optional ordered database operations attached to step IDs. Each operation references a qualified stable object ID, operation kind, input/output data, relevant field IDs when known, conditions, and evidence. Distinguish execution order from data movement. Group transaction boundaries only when verified.
- Optional failure explanations attached to the relevant step or database operation, describing impact, continuation, retries and uncertainty. Use these fields for “What this means in practice”; do not maintain a parallel copy of the workflow.
- Optional presentation metadata grouping stable step IDs into meaningful stages. Keep this grouping separate from execution transitions; it must not change behavior.
- Evidence gaps and any limits on inspection. Empty database operations mean “none verified” unless the source explicitly establishes that no database is involved.

Keep native table names, column definitions, constraints and indexes in their catalog entries. Diagram captions, tables and modals all derive from those entries. Store JSON with consistent indentation, readable field names and limited nesting. Document source ownership near the source inspector so an editor knows which file to change. Reference columns, keys, and indexes in the schema catalog. Do not repeat the full table definition in each use case. A few contextual labels in generated output are acceptable; maintaining duplicate schema descriptions is not.

The index lists IDs, titles, source/page paths, participating object IDs, and concise evidence/coverage status. Derive object references from use-case operations. The index supports selective loading and lookup; it must not become a second manually maintained description of behavior.

## Modular actions linked from tables

Each table page derives its action cards from canonical workflow operations. Show a business title, the operation and a short explanation of its effect on this specific table. One workflow can appear on many table pages, but its explanation and mappings are edited once in its JSON source. Do not copy its full flow into every table page.

A lifecycle action may reference a shared save/recovery workflow by stable ID. Keep the action's trigger, outcome and table-specific effect in its module; keep detailed shared transaction logic in the referenced module. Resolve references when generating mappings and reject missing references or cycles. Distinguish a referenced implementation workflow from an additional user action so it does not become a duplicate action card. A concise action summary can link to the shared flowchart instead of duplicating it. Only add `?database=1` to pages that actually implement the toggle.

The derived index includes each table's individual page, source path and reverse workflow references. Table names and diagram labels come from the catalog; workflow sources reference stable IDs rather than copying schema definitions. Regenerate affected pages and mappings after edits.

## The two views

**Default: business flow.** Show actor and trigger, application steps, decisions, business failures, and outcome. Hide database-specific operations and schema details. Use meaningful business labels derived from the real action, not unexplained code calls. The visible summary describes the action; expandable prose explains consequences without reciting the diagram.

**Expanded: business flow plus database details.** On the same page, preserve the business flow, leave unaffected stages in place, and add exact catalog-named tables/objects, reads, inserts, updates, deletes, data movement, and verified transaction boundaries. Annotate unknown details. When a database error affects the business outcome, the business failure remains visible in both modes while its technical explanation belongs in the expanded view.

Use an actual keyboard-accessible button labeled “Show database details,” changing to “Hide database details” when active. Synchronize `aria-expanded`, `aria-controls`, visibility, and the text fallback. Keep focus on the button. Hidden diagrams must not remain exposed to assistive technology. If a use case has no verified database mapping, explain the evidence status instead of drawing speculative nodes.

Support a stable URL parameter such as `?database=1` for expanded mode and the default URL for business mode. Initialize from the URL and keep state correct on back/forward navigation. Table links to flow pages target expanded mode; links to summary modules use their normal URLs. General application links target default mode. Make table nodes open an accessible details modal using trusted local handlers and stable catalog IDs; keep Mermaid in strict mode. Retain ordinary adjacent catalog links as fallback navigation. Read [html-format.md](html-format.md) for the modal, navigation and styling contract.

Generate staged Mermaid diagrams and their database-expanded variants from the same source. Prefer pre-rendered inline SVGs with a small local JavaScript toggle, preserving portable offline reading. Ensure every SVG element ID and reference is unique across all stages and variants. Use progressive enhancement: without JavaScript, both labeled views and their text explanations remain readable. Printing should include the selected view and its label; the no-JavaScript fallback can print both.

## Token-efficient changes

For initial documentation, build the full inventory and shared index once. For later edits:

1. Read the index and the changed code/schema scope.
2. Load affected use-case sources and referenced schema entries. Expand the set only where dependencies require it.
3. Update the canonical sources, then regenerate affected pages and derived reverse mappings.
4. Check links, references, and coverage mechanically across the index. Read additional content when inconsistencies appear.

A table rename may affect multiple use cases; a UI label change may affect only one. Remove obsolete derived mappings when operations are removed. Detect missing or stale index entries before relying on selective loading. Do not claim token savings as measured without a comparison; the design reduces duplicated authoring and repeated context loading.


## Where to make a change

| Requested change | Authoritative place to edit |
| --- | --- |
| New step, decision, failure, outcome, or business explanation | The affected use-case JSON record. |
| A step reads or writes a different table | That step's database operations; regenerate reverse mappings. |
| Column, key, index, or table name changes | The relevant table JSON definition and affected stable references. |
| Different stage grouping | Presentation metadata referencing existing step IDs. |
| Layout, row shading, or typography | Shared presentation styles/template. |
| Navigation, database toggle, or modal behavior | Shared interaction code. |

Do not hand-edit generated Mermaid/SVG/HTML as the only fix. Update the source or renderer and regenerate affected output. If an artifact must be patched during a blocked preview session, apply the same change to its source/renderer and reconcile the generated result before calling the workflow reusable. Do not publish machine-specific paths or temporary build dependencies as reusable installation instructions.
