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
   - Each phone is a device frame around an `<iframe>` sized to the selected model's CSS viewport from the tables below, then scaled with `transform` so both phones fit the window together. The iframe keeps the true viewport, so media queries and `vw` units behave as on the device.
   - Live source: both iframes load the URL. Otherwise each iframe gets the screen through `srcdoc`.
   - Above each phone, a `<select>` with that platform's models, grouped by tier (low, mid, high, fold) and showing the name and viewport (`Galaxy S10 · 360×760`). Changing it resizes that phone only, animated.
   - A toolbar with: portrait/landscape, light/dark, and a **sync** toggle that mirrors scroll position between both phones.
   - The URL hash keeps both models, the orientation, and the theme, so a reload restores the same comparison.
   - Inline CSS and JS only; no build step, no external scripts.

3. Draw each frame as the model's real **hardware**, taken from its row in the tables below, because the hardware decides how much of the screen is usable and where content collides:
   - The cutout with its real shape, size, and position: notch, Dynamic Island, punch-hole, or none. It is drawn over the screen with a thin outline, so it stays visible on a dark screen and content that slides under it is visibly hidden.
   - The screen's corner radius, and the bezel: thin and even on all-screen models; a forehead with earpiece and a chin with the home button on iPhone SE and Galaxy J2 Prime.
   - The status bar at the model's top inset, and the bottom system area: home indicator, gesture bar, or 3-button navigation.
   - The insets reproduced as padding inside the iframe (`env(safe-area-inset-*)` on iOS, system bars on Android).
   - On a fold model's open screen, the hinge crease as a thin line down the middle, so content it crosses is visible.
   - In landscape the hardware rotates with the phone: the cutout sits on the left edge, its inset moves to the sides, and the iOS status bar hides.

4. When the screen is rebuilt or designed (not live), render it **native** to each platform from the same content and task:
   - Android follows Material 3: Roboto, top app bar with left-aligned title, FAB, bottom navigation bar, ripple feedback, system back gesture.
   - iOS follows the Human Interface Guidelines: system font (`-apple-system`), large centered or collapsing title, tab bar, back chevron with swipe-back, sheets that slide from the bottom.
   - Both keep the main task working: inputs respond, buttons change state, empty and error states reachable.
   - Touch targets 48dp or more on Android and 44pt or more on iOS; contrast 4.5:1 or more; no horizontal scroll at any model in the tables.

5. Check every model in both selectors: the screen fits with no clipped content or overlapping chrome. Fix what breaks, and report what only breaks on the live source.

6. Save the file in the screen's project (e.g. `docs/ux/`). When the current folder belongs to an unrelated project, save it in a temp folder instead and say so. Open it. Tell the user the path, the source used, and a table of the differences between both platforms, with the models where something breaks first.

## Models

Portrait values in CSS px, grouped by **tier**. Each selector groups its models by tier with `<optgroup>` and defaults to the first mid model. Viewports are exact unless marked; cutout sizes and radii are close approximations.

| Tier | iOS | Viewport | Cutout | Corner radius | Inset top / bottom | Bottom |
|---|---|---|---|---|---|---|
| Low | iPhone SE (3rd gen) | 375×667 | None; forehead and chin bezels | 0 | 20 / 0 | Round home button in the chin |
| Low | iPhone 11 | 414×896 | Wide notch, 209×30 | 41 | 48 / 34 | Home indicator |
| Mid | iPhone 14 | 390×844 | Narrow notch, 162×34 | 47 | 47 / 34 | Home indicator |
| Mid | iPhone 13 mini | 375×812 | Narrow notch, 162×34 | 44 | 50 / 34 | Home indicator |
| High | iPhone 15 Pro | 393×852 | Dynamic Island, 126×37, 11 from top | 55 | 59 / 34 | Home indicator |
| High | iPhone 16 Pro Max | 440×956 | Dynamic Island, 126×37, 14 from top | 62 | 62 / 34 | Home indicator |
| Fold | iPhone Duo (cover) | 466×678 (estimate) | Punch-hole, center (estimate) | 40 | 44 / 34 | Home indicator |
| Fold | iPhone Duo (open) | 890×626 (estimate) | None; hinge crease | 36 | 24 / 21 | Home indicator |

| Tier | Android | Viewport | Cutout | Corner radius | Inset top / bottom | Bottom |
|---|---|---|---|---|---|---|
| Low | Galaxy J2 Prime | 360×640 | None; forehead and chin bezels | 0 | 24 / 0 | Physical home button and 2 capacitive keys in the chin |
| Low | Galaxy A05 | 360×800 | U notch, center | 18 | 28 / 48 | 3-button navigation |
| Mid | Galaxy A54 | 360×780 | Punch-hole, center | 26 | 32 / 24 | Gesture bar |
| Mid | Pixel 7a | 412×915 | Punch-hole, center | 28 | 32 / 24 | Gesture bar |
| High | Galaxy S23 | 360×780 | Punch-hole, center | 28 | 32 / 24 | Gesture bar |
| High | Galaxy S10 | 360×760 | Punch-hole, top right | 30 | 32 / 24 | Gesture bar |
| High | Pixel 8 Pro | 448×998 | Punch-hole, center | 36 | 32 / 24 | Gesture bar |
| Fold | Galaxy Z Fold 5 (cover) | 344×882 | Punch-hole, center | 20 | 32 / 24 | Gesture bar |
| Fold | Galaxy Z Fold 5 (open) | 690×829 | None; hinge crease | 22 | 32 / 24 | Gesture bar |

Apple sells no low tier: its low models are the oldest and smallest still in use. The low tier is where a layout breaks first, so step 5 starts there.

The iPhone Duo viewports are Apple's published pixels (1398×2034 cover, 1878×2670 open) divided by an assumed 3x scale, and its hardware is estimated: replace them when Apple documents the points.

When the user names a model outside the tables, add it to its tier with its real viewport and hardware.

The file is done when both phones show the same screen, every frame matches its model's row, every model in both selectors passes step 5, and the hash restores the comparison.
