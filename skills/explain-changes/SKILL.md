---
name: explain-changes
description: Explain edited files, diffs, or a requested change set in clear plain language, followed by an evidence-backed file-by-file breakdown. Use when a user asks what changed, how a patch works, or for a change summary; do not use for code review or implementation unless separately requested.
---

# Explain Changes

Inspect the actual diff and relevant surrounding code before explaining it. Treat prior summaries as context, not evidence.

Begin with a concise but thorough plain-language overview. Explain:

- what changed;
- why the change was needed;
- how the resulting behavior or workflow now operates;
- important consequences, tradeoffs, limitations, prerequisites, or unchanged behavior.

Write for a reader who understands the project but may not know the implementation details. Define unavoidable technical terms briefly. Lead with behavior and outcomes rather than filenames or line-level mechanics.

After the overview, provide a clear breakdown organized by file. Follow the same presentation pattern for every file:

1. Use the file path or filename as the heading.
2. In the first paragraph beneath that heading, describe in simple language what changed in that file, why it changed, and the practical effect. Make this paragraph understandable without requiring the reader to interpret implementation details.
3. After the descriptive paragraph, provide the technical information as concise bullets or a clearly labeled technical-details section. Include relevant functions, variables, conditions, commands, data flow, failure behavior, or tests, but only when supported by the inspected diff.

Do not begin a file entry with raw implementation details or a bullet list. The explanatory paragraph must come first for every file, including tests, documentation, configuration, and generated artifacts. Group files only when the user asks for grouping or when multiple generated artifacts have no meaningful independent behavior; otherwise explain each changed file separately.

Distinguish these categories whenever they are present:

- deliberate source or configuration changes for the requested work;
- tests and what meaningful behaviors they verify;
- documentation updates;
- earlier, unrelated, or pre-existing dirty changes;
- generated, cached, incidental, or otherwise questionable commit artifacts.

Ground every claim in the inspected diff. Check staged, unstaged, and untracked changes as relevant, and compare against the appropriate base when the requested change set is committed. Do not attribute a pre-existing modification to the current task without evidence. Call out uncertainty or unavailable evidence instead of guessing.

Keep the explanation concise while retaining behaviorally important details. Avoid dumping diff syntax, narrating trivial formatting, or listing every changed line. Mention verification results only when they were actually run or are visible in reliable evidence.

This skill is explanatory and read-only. Do not modify files, perform an adversarial review, commit, push, or broaden the task unless the user separately requests that action.
