---
name: mobile
description: "Preview one screen on Android and iOS side by side in a single HTML file, with a phone model selector on each."
argument-hint: "What screen to preview (e.g. login of the delivery app, or http://localhost:3000/checkout)"
disable-model-invocation: true
---

The user wants to see how **one screen** looks on **Android and iOS at once**: two phones side by side in **one HTML file**, each with its own model selector, so they can judge both platforms while the design evolves.

## Steps

1. Find the **source** of the screen, in this order, and stop at the first that applies:
   - A URL or running dev server in the arguments or the conversation: the **live** source. Check it responds before using it.
   - A screen in the working repo (route, component, React Native or Flutter view) matching the arguments: read it with its design tokens (CSS variables, Tailwind config, theme files) and rebuild it as HTML with its real copy, data shape, colors, and fonts.
   - A description only: design the screen, inventing realistic data (names, amounts, dates).
   Then state in 3 lines the screen, the user, and the one task it serves, with the source of each. Ask only when the context leaves the screen unknown.

2. Build one self-contained `.html` file with two **phones**, Android on the left and iOS on the right:
   - Each phone is a device frame around an `<iframe>` sized to the selected model's CSS viewport from the table below, then scaled with `transform` so both phones fit the window together. The iframe keeps the true viewport, so media queries and `vw` units behave as on the device.
   - Live source: both iframes load the URL. Otherwise each iframe gets the screen through `srcdoc`.
   - Above each phone, a `<select>` with that platform's models, grouped by tier (low, mid, high) and showing the name and viewport (`Galaxy S10 · 360×760`). Changing it resizes that phone only, animated.
   - A toolbar with: portrait/landscape, light/dark, and a **sync** toggle that mirrors scroll position between both phones.
   - The URL hash keeps both models, the orientation, and the theme, so a reload restores the same comparison.
   - Inline CSS and JS only; no build step, no external scripts.

3. Draw each frame's **system chrome** for the selected model, because it decides how much of the screen is really usable:
   - iOS: status bar with notch or Dynamic Island, home indicator, and `env(safe-area-inset-*)` reproduced as padding inside the iframe. iPhone SE has a home button and no insets.
   - Android: status bar with a punch-hole camera, and the gesture bar or 3-button navigation at the bottom.

4. When the screen is rebuilt or designed (not live), render it **native** to each platform from the same content and task:
   - Android follows Material 3: Roboto, top app bar with left-aligned title, FAB, bottom navigation bar, ripple feedback, system back gesture.
   - iOS follows the Human Interface Guidelines: system font (`-apple-system`), large centered or collapsing title, tab bar, back chevron with swipe-back, sheets that slide from the bottom.
   - Both keep the main task working: inputs respond, buttons change state, empty and error states reachable.
   - Touch targets 48dp or more on Android and 44pt or more on iOS; contrast 4.5:1 or more; no horizontal scroll at any model in the table.

5. Check every model in both selectors: the screen fits with no clipped content or overlapping chrome. Fix what breaks, and report what only breaks on the live source.

6. Save the file in the screen's project (e.g. `docs/ux/`). When the current folder belongs to an unrelated project, save it in a temp folder instead and say so. Open it. Tell the user the path, the source used, and a table of the differences between both platforms, with the models where something breaks first.

## Models

CSS viewport in portrait, width × height, grouped by **tier**. Each selector groups its models by tier with `<optgroup>` and defaults to the first mid model.

| Tier | Android | Viewport | iOS | Viewport |
|---|---|---|---|---|
| Low | Galaxy J2 Prime | 360×640 | iPhone SE (3rd gen) | 375×667 |
| Low | Galaxy A05 | 360×800 | iPhone 11 | 414×896 |
| Mid | Galaxy A54 | 360×780 | iPhone 14 | 390×844 |
| Mid | Pixel 7a | 412×915 | iPhone 13 mini | 375×812 |
| High | Galaxy S23 | 360×780 | iPhone 15 Pro | 393×852 |
| High | Galaxy S10 | 360×760 | iPhone 16 Pro Max | 440×956 |
| High | Pixel 8 Pro | 448×998 | | |
| High | Galaxy Z Fold 5 (cover) | 344×882 | | |

Apple sells no low tier: its low models are the oldest and smallest still in use. The low tier is where a layout breaks first, so step 5 starts there.

When the user names a model outside the table, add it to its tier with its real viewport.

The file is done when both phones show the same screen, every model in both selectors passes step 5, and the hash restores the comparison.
