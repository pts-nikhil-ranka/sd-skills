---
name: production-readiness-change-brief
description: Create a dated, data-driven HTML change brief from code-review or production-readiness findings. Use when the user wants concise before/after discussions, implementation plans, and file-touch reasons in a reusable HTML plus JSON format; do not use for filing GitHub issues or implementing the fixes.
---

# Production Readiness Change Brief

Create a readable review artifact without changing application code.

## Workflow

1. Confirm the findings from code evidence or the user's supplied review. Keep distinct defects as distinct changes.
2. Use the current local date and a short lowercase purpose slug. Unless the user specifies another location, create `reviews/production-readiness/` in the repository.
3. Copy [assets/master-review.html](assets/master-review.html) to `YYYY-MM-DD-<purpose>-review.html`.
4. Read [references/report-schema.md](references/report-schema.md), then create a matching `YYYY-MM-DD-<purpose>-review.json` beside the HTML. The basenames must match so the viewer can load the data automatically when served over HTTP.
5. For each change, write three clearly separated explanations:
   - what happens without the change;
   - what the change will do;
   - how it will be implemented, including every expected file and why it is touched.
6. Validate the JSON, check the embedded JavaScript syntax, serve the directory locally, and inspect the rendered desktop and narrow-screen layouts. Test JSON loading, priority filters, and print behavior. If direct `file://` access blocks JSON fetches, verify the built-in file picker as the fallback.

## Writing constraints

- Prefer concrete failure scenarios and outcomes over generic risk language.
- Keep current behavior separate from the proposed design; do not claim unimplemented work already exists.
- Explain file touches at responsibility level, not merely as a filename list.
- Include acceptance checks when they make failure and recovery behavior observable.
- Keep findings in JSON only. The HTML asset owns structure, CSS, rendering, filtering, and print behavior.
- Preserve the user's repository and application worktree except for the requested report files.
