# Report JSON schema

The HTML viewer expects UTF-8 JSON with this shape. Additional fields are allowed, but the required fields must remain stable.

```json
{
  "schemaVersion": 1,
  "report": {
    "type": "Production-readiness change brief",
    "title": "Human-readable title",
    "date": "YYYY-MM-DD",
    "purpose": "Why this report exists",
    "repository": "owner/repository or local repository name",
    "scope": "Reviewed scope",
    "summary": "One concise summary paragraph"
  },
  "changes": [
    {
      "id": "stable-lowercase-slug",
      "priority": "P1",
      "title": "Direct change title",
      "withoutChange": "What happens today and the concrete consequence.",
      "withChange": "The intended behavior after implementation.",
      "implementation": {
        "approach": "The design direction and safety invariant.",
        "steps": [
          "A short implementation step"
        ],
        "files": [
          {
            "path": "path/from/repository/root",
            "reason": "Why this file must change"
          }
        ]
      },
      "acceptanceChecks": [
        "An observable result that proves the change works"
      ]
    }
  ]
}
```

## Required content

- `report.title`, `report.date`, and `report.purpose` identify the artifact.
- `changes` contains one entry per independently actionable change.
- `withoutChange`, `withChange`, `implementation.approach`, and at least one `implementation.files` entry are required for every change.
- Priorities should use `P1`, `P2`, or another short project convention. The viewer renders `P1` and `P2` with dedicated colors and handles other values safely.
- File paths are repository-relative unless the user explicitly requests absolute paths.

## Filename contract

Use identical basenames:

```text
YYYY-MM-DD-purpose-review.html
YYYY-MM-DD-purpose-review.json
```

The HTML derives the JSON filename from its own name. A different data file can be selected with `?data=<relative-json-path>` or through the visible file picker.
