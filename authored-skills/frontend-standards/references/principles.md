# Frontend Principles

These standards apply across projects, technologies, and coding agents. All rules are **mandatory when applicable**. Exceptions must be explicitly identified and justified; do not silently omit a rule.

## FE-001 — Loading feedback for API-triggering buttons

**Trigger:** A user activates a button that starts an API/network request.

**Requirements:**

1. Immediately upon starting the request, disable that button to prevent repeated activation while the request is in flight. Guard against duplicate invocation in the event handler, not only through a visual disabled state.
2. Show a visible loading spinner **inside the button, before its existing text**, while the request is pending. Preserve the button label; do not replace it with spinner-only content.
3. Keep the button disabled and spinner present until the action's request lifecycle finishes.
4. On **both success and failure** (including rejected promises, network errors, and handled cancellation), remove the spinner and release the temporary loading-disabled state. A `finally`-equivalent cleanup is generally appropriate.
5. Preserve other reasons for disabling the button. Completing a request must not enable a control that is still disabled due to form validation, permissions, or other conditions.
6. Communicate the pending state accessibly as appropriate to the control and surrounding UI; a spinner's visual appearance alone is insufficient. Avoid layout shifts when it appears.

**Acceptance criteria:**

- Starting an API call shows a spinner before the button text and prevents duplicate requests.
- While pending, the button is disabled.
- After a successful response, the spinner disappears and the loading-disabled state clears.
- After a failed response or cancellation, the same cleanup happens and the user can retry if otherwise permitted.
- The accessible button name remains understandable during loading.

## FE-002 — WCAG 2.1 Level AA accessibility

**Trigger:** Any frontend UI is created, changed, or reviewed.

**Requirements:**

1. Design and implement against **all applicable WCAG 2.1 Level A and AA success criteria**, not merely isolated ARIA checks. Prefer native semantic elements and correct HTML labeling; add ARIA attributes where native semantics do not already provide what is needed.
2. Ensure all relevant actions and interactive components are operable by keyboard alone, with a predictable focus order and visible focus indicators. Provide appropriate skip navigation and avoid keyboard traps, except intentional focus containment within active modal dialogs.
3. For actual modal dialogs: expose appropriate dialog semantics and accessible name; move focus into the dialog when opened; keep keyboard focus within it while active; support appropriate keyboard dismissal; and return focus to a sensible origin when closed.
4. Support screen readers: accessible control names, roles, states, form instructions, errors, and announcements of meaningful dynamic changes, including loading outcomes and user-action status. Use `role="status"` / polite live regions for nonurgent status and assertive alerts only when warranted; avoid unnecessary focus stealing.
5. Honor applicable contrast, non-text contrast, text resizing, reflow, input purpose, error identification, pointer, timing, and other WCAG 2.1 AA requirements. Do not treat this list as exhaustive.
6. Evaluate the full interaction in success, error, loading, empty, and modal states, including at mobile widths and with increased zoom/text size.

**Acceptance criteria:**

- No known applicable WCAG 2.1 A/AA violations remain in the work being shipped, or exceptions are clearly documented for resolution.
- Automated accessibility checks are used where available, alongside keyboard-only and manual assistive-technology checks.
- No claim of *verified full WCAG compliance* is made without a sufficiently comprehensive audit; automated scans alone do not establish compliance.

**Normative reference:** https://www.w3.org/TR/WCAG21/
**Implementation quick reference:** https://www.w3.org/WAI/WCAG21/quickref/

## FE-003 — Bottom-right self-dismiss status notifications

**Trigger:** The interface chooses a **temporary floating notification** (sometimes informally called a modal) to show the outcome/status of a user action.

**Requirements:**

1. Place the notification at the **bottom-right** of the viewport, accounting for safe areas and different screen sizes.
2. Keep it visible for a few seconds, then **dismiss automatically**; use a default of **5 seconds** unless the project's requirements call for a different suitably accessible duration.
3. Present simple transient updates as **non-modal toasts/status notifications**, not true modal dialogs that trap focus or block the application.
4. Announce the status accessibly without stealing focus. Provide an appropriate live region for screen readers.
5. Do not auto-dismiss critical errors, actionable prompts, or information users cannot retrieve elsewhere before they can act or understand it. Such content requires a persistent/otherwise accessible presentation. If a toast has focusable actions or a dismiss control, consider pause-on-hover/focus and a longer or persistent lifetime as needed.
6. **If user-action status is shown another way** (e.g. inline text or a persistent panel) **the bottom-right positioning and timed-dismissal requirements do not apply**.
7. A genuine interactive modal dialog must satisfy FE-002 dialog accessibility; it should not be made a bottom-right auto-dismiss toast merely to satisfy this rule.

**Acceptance criteria:**

- A transient floating user-action status appears at bottom-right and dismisses automatically after approximately five seconds.
- The rest of the UI remains interactive and focus is not unexpectedly moved.
- Screen readers can receive the status update.
- Critical/action-required information stays available and does not disappear solely because a short timer elapsed.
- Interfaces that do not use a temporary floating status notification are not forced to create one.
