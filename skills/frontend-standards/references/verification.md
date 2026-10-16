# Frontend Standards: Verification Checklist

Apply checks to new and modified UI. Choose the project's existing tooling where possible, and state any untested requirements in the completion report.

## FE-001 — API-button behavior

- [ ] Start an API request and assert the initiating button becomes disabled immediately.
- [ ] Assert the spinner is visibly before the existing label **inside** that button.
- [ ] Attempt rapid repeated activation and assert no duplicate request is sent for the same pending action.
- [ ] Resolve the request and assert spinner removal and loading-state cleanup.
- [ ] Reject the request / simulate a network error and assert identical cleanup and an available retry where otherwise allowed.
- [ ] Exercise cancellation if supported. Verify a pre-existing independent disabled condition is preserved.
- [ ] Check readable accessible button name and status information during loading.

For JavaScript frameworks, use component and integration tests with controlled/blocked promises rather than a fixed sleep. Prefer cleanup in a `finally`-equivalent and prevent state writes after unmount if relevant.

## FE-002 — WCAG 2.1 AA

- [ ] Run available automated audits (for example axe-core) and resolve reported issues.
- [ ] Check keyboard-only navigation, operation, logical focus order, and visible focus.
- [ ] Open/close each relevant modal by keyboard; confirm dialog labeling, initial/contained focus, appropriate Escape handling, and focus restoration.
- [ ] Validate form labels, help text, validation errors, and announcements.
- [ ] Test dynamic status announcements and screen-reader use where tools are available (e.g. VoiceOver and/or NVDA).
- [ ] Check relevant contrast ratios and usable responsive reflow/zoom.
- [ ] Manually review applicable WCAG 2.1 A and AA success criteria that automated tools cannot reliably detect.

Automated reports are evidence of checks performed, **not** certification of comprehensive WCAG compliance.

## FE-003 — Transient status notifications (only if used)

- [ ] Trigger a user action and check the temporary floating notification is at the bottom-right on desktop and mobile.
- [ ] Use a deterministic/fake clock in tests to verify the default ~5-second self-dismiss.
- [ ] Verify non-modality: focus remains where expected and other controls stay usable.
- [ ] Verify accessible live announcement of the status.
- [ ] Verify essential, critical, or actionable information does not disappear before users can consume or act on it.
- [ ] Check focus/hover behavior when the notification contains interactive controls.
- [ ] If feedback is inline or persistent instead of floating, mark FE-003 as not applicable rather than adding an unnecessary toast.

## Completion reporting

Summarize which rules applied; list executed checks, their results, and unverified manual checks or open exceptions. Never report tests as passed unless they were actually executed.
