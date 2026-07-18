Base surface for everything. Flat hairline by default; add `elevation` to lift focal cards, `accent` for a score-family rail.

```jsx
<Card accent="var(--repair)" elevation="raised" pad="lg">
  <CardHeader eyebrow="Result Plot 01" title="Support by archetype" />
  …content…
</Card>
```

`elevation`: flat | raised | floating. `pad`: none | sm | md | lg. Keep most cards flat; reserve `floating` for dialogs/popovers.
