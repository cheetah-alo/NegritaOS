A 0–100 pressure score as a calm horizontal meter with a big mono value.

```jsx
<ScoreMeter family="repair" value={62} />
<ScoreMeter family="risk" value={38} threshold={55} thresholdLabel="≥55 → D" />
<ScoreMeter family="operational" value={74} size="lg" />
```

`threshold` draws the archetype-promotion line (e.g. ≥55). `family`: repair | risk | operational.
