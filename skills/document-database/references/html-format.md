# HTML presentation and interaction contract

This is the refined format from the repository-backed design review. Preserve its information hierarchy and interactions when producing future guides. Adapt branding, domain terms, section count, and actual content to the application. Do not copy Flip Trading behavior into unrelated guides.

Use Mermaid for flowcharts, compiled Tailwind CSS for styling, and small local JavaScript for interactions. [../assets/guide.css](../assets/guide.css) preserves the reviewed presentation: navy header, light neutral page, blue accents, numbered stage cards, striped tables, a compact section rail, business explanations, and a table modal. Reuse or adapt these styles with the component structure below. Keep CSS in a shared asset or embed it at build time. Do not load or duplicate the whole stylesheet into every authoring prompt.

## Page structure

The primary entry point is the database, not an individual use case:

1. **Directory:** brief database purpose and scope, then links to individual table pages. Do not embed schema tables here.
2. **One table per HTML file:** exact table name, a practical question it answers, and a short visible explanation of what one row means and why the table matters. Add an interpretation note where it prevents a likely misunderstanding.
3. **Structure and actions:** columns on the left; every verified action that reads or changes this table on the right. Each action shows a short business title, operation labels and the specific effect on this table. Link it to its canonical use-case page. Keep keys/indexes and source evidence available progressively. Link related tables to their own pages.
4. **Maintenance:** identify this table's JSON source and shared action sources. Derive reverse mappings; do not author a second action list.

Account for application actions, background recovery, storage setup and reporting where verified. Distinguish an available reporting view from an observed application reader. Do not invent update, rename or delete actions to fill a CRUD checklist. State which operations were not found and the inspected scope. A table's action list is a support map, not execution order.

Use this reading order for an independently readable use-case page:

1. **Overview:** application identity, concise use-case title, one-line purpose, and a visible paragraph explaining the real action in business terms. State who/what starts it, what happens, and the outcome. Place a compact trigger/scope panel alongside it. Show source revision and verification status without implying live validation.
2. **Workflow:** numbered, connected stages when a single chart would be tall or tangled. The database-details button belongs beside the workflow heading.
3. **Business explanation:** an expandable “What this means in practice” section. Give context, consequences, and failure handling beyond what the flowchart labels already convey.
4. **Table access:** link each participating table to its individual HTML page. Clicking a table in the diagram opens the shared table-details modal. Do not turn the use-case page into a second multi-table catalog; modal contents derive from the same catalog sources.
5. **Maintenance and evidence:** clearly identify the editable use-case and table sources. Offer JSON inspection and source references progressively, keeping implementation detail out of the opening explanation.

Account for every in-scope table in the directory. Use-case pages may involve multiple tables, but each table’s full documentation has its own canonical HTML page.

Match existing terminology and documentation conventions. Explain unfamiliar database terms briefly when needed. Never mark an invented scenario as repository-verified. Review examples should use an actual application/EA action when repository source is available; describe unverified portions as gaps.

## Component structure and styling

The supplied CSS uses these classes; they describe presentation, not a required frontend framework:

- `.topbar`, `.brand`, `.brand-mark`: compact application header. Do not add a duplicate top section menu when the dot navigation already serves that purpose.
- `main > #overview.hero`: `.eyebrow`, heading, `.lead`, `.use-case-summary`, `.meta`, plus `.context` for the trigger/scope.
- `.section-heading`: section number/name and optional action button.
- `.stage-grid > .stage`: `.stage-head` with `.stage-number`, title and brief subtitle; `.diagram` holds a Mermaid SVG.
- `.db-details`: database-specific explanation shown with the database layer. `.takeaway` may emphasize one important consequence, without repeating the whole narrative.
- `.business-guide`: native `details`/`summary`; `.guide-body`, `.guide-columns`, `.business-steps`, `.failure-guide`, `.guide-outcome`, and `.meaning-note` organize explanatory prose.
- `.schema-card`: `.schema-heading` followed by `.schema-layout`; `.table-wrap` holds the semantic table and `.table-aside` holds actions and supporting structure.
- `.source-grid > .source-card`: links to editable sources and an optional JSON disclosure. `.quiet-details` holds evidence.
- `.section-rail`: viewport-centered navigation. `.table-dialog`: a native table-details modal.

Use restrained contrast and enough spacing to scan. Keep column names/code identifiers distinct from prose. Table rows alternate light neutral fills, with a subtle hover highlight and a contrasting header. Use semantic column/row headers. Primary/foreign key badges must reflect actual schema facts; never assume the first column is a primary key. Avoid gratuitous badges or decorative status claims.

Stack stage cards, schema panels, and maintenance cards at narrow widths. Keep diagram labels readable; adjust grouping/layout before shrinking text. Long table identifiers may wrap but must remain complete. A wide schema table may scroll horizontally inside its own container while the page remains within the viewport. Include visible keyboard focus and usable print styles. If sorting is provided, inactive columns show neutral paired arrows; only the active sort shows its actual direction and `aria-sort` state.

## Fixed dot navigation

Reuse [../assets/section-rail.html](../assets/section-rail.html), [../assets/section-rail.js](../assets/section-rail.js), and the rail rules in `guide.css` together. Generate the links from the page's actual section IDs and labels. The link is the hit area; its child `.rail-dot` is the small circle and `.rail-label` is the label. Never style the link itself as a circle while retaining `.section-rail a` layout rules. Remove conflicting rail overrides instead of layering a second component over them. Use this component on table and workflow pages; a short directory need not have a rail.

Use a small fixed rail on the left, with one dot per major section. It occupies minimal width at rest. Hover or keyboard focus reveals section names in a compact panel without shifting the page. Clicking a link scrolls to its section. Highlight the current section and expose `aria-current="location"`; update it during scrolling and after navigation.

Center the **dot group vertically within the visible browser viewport**, not within document content, a large page wrapper, or the full scrollable page. It must remain centered during scrolling and viewport resizing. Use `position: fixed` and a half-height translation with a dynamic viewport midpoint. For visual-viewport changes, a suitable calculation is `visualViewport.offsetTop + visualViewport.height / 2`, falling back to `innerHeight / 2`. Use `50dvh` as the CSS fallback. Do not introduce arbitrary offsets such as 44%.

Place a touch-only expand/collapse button outside the centered dot group's normal layout so its height does not move the dots off-center. Touch expansion, dismissal, focus styles, accessible labels, and reduced-motion behavior must work. Provide enough left gutter so the collapsed rail does not cover document text. Hide it in print.

## Flowcharts and the database layer

A use-case diagram describes execution order. A table-to-action support map describes what a table supports; label it accordingly and do not present its arrows as chronological execution. A support map can use `flowchart LR` with the table on the left and verified action nodes on the right.

For complicated flows, split the view into meaningful numbered stages rather than drawing long arrows across the whole page. Stage count follows the behavior, not a fixed three-stage rule. Keep branches local and label connectors such as “Continue to stage 2” or “Next channel: repeat stage 2.” Every connector must resolve to the same transition as the underlying source graph. Do not lose early exits, failures, loops, or ordering when splitting the chart. Keep full business labels and explanations available in the source and text alternative.

The default view shows business steps, decisions and outcomes. “Show database details” adds database nodes and labeled operations to the relevant stage; it becomes “Hide database details” when enabled. Keep unaffected stages in place, retain the business sequence, and avoid rearranging the entire chart. Both views come from the same source. Support direct expanded links, e.g. `?database=1`, browser back/forward, synchronized accessible state, and a readable no-JavaScript fallback.

**Every table node shows the exact table name from the catalog.** Include its namespace where needed to distinguish objects. Do not replace `notification_delivery_attempts` with a generic label such as “Delivery attempts.” Wrap long identifiers or allocate more room. Reference tables by stable IDs in the source; derive labels from their definitions so renames cannot leave stale captions.

Differentiate execution edges from data-transfer edges with line styles and text. Read data travels from the table to its consuming step; write data travels from the producing step to the table. Explicitly label READ/INSERT/UPDATE/DELETE. Only show transactions, rollback, asynchronous boundaries and relationship cardinality that evidence establishes. If no database read happens, do not invent one to balance a diagram.

Keep Mermaid in strict security mode. Generate safe internal IDs and escape labels. Prefer pre-rendered SVGs with local interactions; runtime Mermaid is optional. Namespace **all** generated SVG IDs and their references across stages and modes, not just each SVG's root ID. Retain a readable text alternative. Never lower security mode just to enable table clicks.

## Clickable tables and modal details

Clicking a table node/name opens a modal containing its exact name, purpose, columns, declarations, business meanings, keys, indexes, relationships, and verified supported actions. Reuse the same table data and renderer as the catalog. Do not maintain a second definition for the modal. Generated DOM may be duplicated; authoritative source content must not be.

Prefer native `dialog` and `showModal()`. Provide an accessible title, a visible Close button, Escape dismissal, outside-backdrop dismissal, scrollable content, background scroll control, and focus restoration to the invoking table node. Repeated open/close cycles must not leave stale table data or a locked page. Cloned content must not introduce duplicate IDs.

Bind trusted local handlers to generated nodes using stable table IDs or a build-time mapping. Make the entire table node interactive, including its text, with a pointer cue, hover/focus treatment, keyboard activation by Enter/Space, an accessible name, and `aria-haspopup="dialog"`. An interactive node must not be hidden from assistive technology by an enclosing `role="img"`; use an appropriate group structure. Retain a normal link to the catalog as a fallback when scripts or modal support are unavailable. Include a brief cue that table nodes can be opened.

## Table content

Explain what one row represents. Preserve exact native columns/types, nullability, defaults/generated expressions, primary/foreign/unique keys, composite key order, check constraints, and relevant lifecycle/ownership facts. Separate indexes from constraints and include ordered columns/expressions, predicates, included columns and native options where present. Do not infer query-plan usage from index existence.

Document related views, triggers, routines, partitions and policies when they materially affect the action. Derive supported actions and their physical database effects from the shared use-case sources. Keep uncertain meanings and undiscovered callers explicit.

## Business explanation

Engaging means useful and immediately understandable, not promotional. Start with the reader's task: “Which settings were in use, and when?” is more helpful than an abstract description of persistence. Use domain-appropriate questions; do not copy this example's trading concepts into other applications.

Use short, complete sentences and familiar verbs. Give actions titles such as “Start a new run” or “Catch up after a delayed save” when the code supports those behaviors. Explain what changes, what stays available, and what the reader can conclude from the stored values. Introduce code identifiers after the business meaning. Avoid noun-heavy labels, vague claims and a paragraph that merely repeats the heading. Preserve technical qualifications without front-loading them.

Table source JSON owns its purpose, optional reader question, introductory paragraph and interpretation note. Workflow source JSON owns its trigger, outcome, failure explanation and per-table effects. Keep the visible copy concise; put detailed mechanics and source evidence behind disclosures or links.

Begin each use case with a short visible paragraph. Under “What this means in practice,” explain the action in a small number of clear business steps: what the operator should expect, why a decision matters, where the result appears, and how to interpret it. Use complete sentences and familiar language.

Describe meaningful failure paths separately: what fails, what is recorded or visible, whether remaining work continues or stops, whether a retry happens, and what remains uncertain. Only make claims supported by source evidence. Distinguish success reported by a subsystem from confirmation of the actual business outcome.

Do not print a second numbered copy of every diagram node or a list of code function names. Keep explanatory text with the relevant canonical use-case steps or structured outcome notes; derive this section from those fields. Keep code evidence available separately. Avoid duplicated facts that require independent edits in a narrative and a workflow.

## Delivery and validation

Use portable HTML with compiled Tailwind CSS and pinned Mermaid versions. Embed CSS/SVG or package local relative assets. Readers should not need Node, a database connection, or network access for the delivered guide. Reuse the project's build tools; do not introduce a server or framework solely for this documentation. Tailwind Play CDN is a prototype-only option, not the durable delivery default.

Check:
- One canonical table HTML file per table; the directory has no embedded schema definitions. Related-table and action links resolve to the correct pages.
- Each table lists all verified in-scope workflows, not only the action used to introduce the example.
- Source completeness, source links, qualified table identities, graph references, and derived action mappings.
- Full identifiers in every database node and matching modal details for every clickable table.
- Readable stage layouts, resolved cross-stage connectors, preserved branches and outcomes, and stable unaffected stages during the toggle.
- Visible introductory paragraph and concise business explanations that add context beyond chart labels.
- Alternating table rows, valid key badges, long names, desktop/narrow layouts, print and offline operation.
- Dot-group midpoint against the visible viewport before/after scrolling, resize, hover and touch expansion; verify rendered bounds instead of only reading `top: 50%`.
- Modal pointer/keyboard opening, focus handling, close/Escape/backdrop dismissal, scroll restoration, multiple table selections and unique IDs.
- Source inspectors show the current JSON; generated content and the maintained renderer agree.

Browser checks use a dedicated new test window. If browser access or dependencies are blocked, do unaffected source/structural checks, honor the restriction, and report which interactions remain unverified. Do not claim visual testing from syntax validation. Do not change technologies solely because one test surface is unavailable.

Official references: [Mermaid flowcharts](https://mermaid.js.org/syntax/flowchart.html), [Mermaid usage/security](https://mermaid.js.org/config/usage), [Tailwind installation](https://tailwindcss.com/docs/installation), [Tailwind Play CDN](https://tailwindcss.com/docs/installation/play-cdn).
