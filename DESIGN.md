---
version: alpha
name: TubeRush TV
components:
  quality-menu:
    owner: YouTube TV overlayPanelItemListRenderer
omitted:
  - section: colors
    reason: Native TV owns surfaces/focus; scoped status colors are documented below.
  - section: typography
    reason: Native scale is retained; scoped Quality variants are documented below.
  - section: rounded
    reason: Inherited from the native TV renderer.
  - section: spacing
    reason: Inherited from the native TV renderer.
---

# TubeRush TV design context

Product for Android TV, operated with a directional remote; Portuguese is the
language of this requested workflow. Preserve the established YouTube TV visual
identity shown in physical screenshots. No rebrand, CSS overlay or new font.

The canonical owner of Quality is the native `quality-selector` modal,
`overlayPanelItemListRenderer` and `compactLinkRenderer`. The fork supplies data
and selection commands; the host owns colors, type, spacing, scrolling and focus.
No separate runtime token adapter is needed because no new style values exist.

The user selected the Limpo preview on 2026-11-18. Later physical testing exposed
one provisional frame on reopening with the custom decoration. The user had
explicitly preferred a stable native menu if the custom skin was unreliable.
The active implementation therefore uses only the native renderer, with complete
title/subtitle supplied synchronously in one dispatch. No custom stylesheet,
MutationObserver, HDR badge, right-aligned lock or post-render decoration remains.

Each row has two lines: resolution, HDR when applicable and fps; then codec,
localized Mbps and a short limit/unavailability indicator. Native spacing and
focus styling apply. No slash separators or bitrate-explanation paragraphs.
Automática has no subtitle. Owner: scripts/quality_formats.js menu/present.
If catalogue data is unavailable, retain the original command without a late swap.

Physical tests: 100 programmatic openings of the native quality renderer with
2,245 frame samples and no provisional list recorded; separately 100 ADB DPAD
commands retained focus inside the menu. These are not 100 full remote-control
paths from playback settings and do not establish long-playback stability.

Limits continue enforced by command handler. Checkmarks require actual playing
format, not just pending selection. No authentication or transport URLs in labels.

Behaviour is defined in docs/plans/2026-11-18-quality-formats-design.md, approved
by the user. Physical validation must include long lists, blocked rows, existing
focus/Back, navigation to another video and confirming actual codec/itag.
