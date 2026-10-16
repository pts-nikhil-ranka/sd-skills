---
name: frontend-standards
description: Apply mandatory, tool-neutral frontend development standards whenever creating, modifying, reviewing, or testing user-facing interfaces, including API button loading states, WCAG 2.1 AA accessibility, and transient status notifications.
---

# Frontend Standards

Use this skill for all frontend implementation and review tasks, regardless of framework or coding agent. These are project-independent mandatory standards. Project conventions may determine *how* to implement them, but may not silently override them.

## Required workflow

1. Read [references/principles.md](references/principles.md) before making frontend changes; implement every applicable rule.
2. For any API-triggering button, apply **FE-001**.
3. Apply **FE-002** to all new or modified UI, including accessibility of loading and feedback states.
4. Apply **FE-003** only when presenting user-action feedback as a temporary floating notification; do not force notifications into otherwise inline interfaces.
5. Before declaring work complete, follow [references/verification.md](references/verification.md). Test applicable success and failure paths, keyboard interactions, and accessible announcements.
6. Report which checks ran and which could not run; never claim complete WCAG compliance from automated tools alone. If requirements conflict, preserve accessibility and call out the conflict and exception for review.

These standards are intended to be expanded with additional numbered rules. Keep the numbered rule IDs stable and place detailed requirements in the references, not in tool-specific instruction files.
