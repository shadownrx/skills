---
name: example
description: "Generate 10 different UI/UX versions of one screen in a single HTML file, to compare and pick."
argument-hint: "What screen to design (e.g. checkout for an ISP plan)"
disable-model-invocation: true
---

The user wants **10 versions** of one screen, side by side in **one HTML file**, so they can compare and pick a direction. Each version is a real design answer, not a recolor.

## Steps

1. Read the **context** before designing, in this order, and stop when the screen is clear:
   - The arguments and the current conversation: what the user is building, for whom, and on which device.
   - The working repo: `README`, `package.json` or equivalent, design tokens (CSS variables, Tailwind config, theme files), and the routes or components whose names match the arguments. Reuse their real copy, data shape, colors, fonts, and components.
   - Other repos or products the arguments name (e.g. a GitHub repo of the user's): read their README for purpose and platform.
   - The **platform** decides the interaction model: TV or console means 10-foot UI with D-pad focus and no hover; mobile means thumb reach and bottom actions; desktop means keyboard and density.
   Then state in 3 lines the screen, the user, and the one task it serves, with the source of each. Ask only when the context leaves the task or platform unknown. When the arguments name a product you cannot find, ask where its project lives before assuming what it is. Invent missing data realistically (names, amounts, dates), never lorem ipsum.

2. Plan 10 versions that differ in **structure**: each one bets on a different UX pattern (for example: single column, split view, wizard, cards, table, dashboard, conversational, command palette, progressive disclosure, mobile-first bottom sheet). Write each bet as one line before coding.

3. Build one self-contained `.html` file:
   - A sticky switcher with the 10 names; keys `1`–`0` and `←`/`→` change version; the URL hash keeps the current one.
   - Each version is a full screen with its main task working (inputs respond, buttons change state, empty and error states reachable).
   - Shared CSS tokens on `:root` for color, spacing, radius, and type, with a dark theme under `prefers-color-scheme`.
   - Inline CSS and JS only; no build step, no external scripts.
   - **Motion** that explains change: version switches crossfade and slide (View Transitions API with a CSS fallback); content enters with a short stagger; selections, toggles, and totals animate (numbers count up); buttons press, load, and resolve into success or an error shake; sheets, steps, and accordions slide. Durations 150–400ms, ease-out, `transform` and `opacity` only; everything stops under `prefers-reduced-motion`.

4. Apply these UX rules in every version:
   - One primary action per screen, visually first.
   - Clear hierarchy: 1 heading level per section, scannable labels, numbers right-aligned.
   - Feedback for every action, animated: hover, focus ring, loading, success, error with the fix.
   - Accessible: semantic HTML, labels on inputs, keyboard reachable, contrast 4.5:1 or more.
   - Responsive for the platform: on web, works at 375px with no horizontal scroll and touch targets 44px or more; on TV, every action is reachable with arrows and Enter, with a visible focus.

5. Under each version's switcher name, show its bet in one line and its main tradeoff.

6. Save the file in the screen's project (e.g. `docs/ux/`). When the current folder belongs to an unrelated project, save it in a temp folder instead and say so. Open it. Tell the user the path, the 10 bets in a table, and your recommended version with the reason.

Every version passes step 4 and differs from the others in structure, not only in color.
