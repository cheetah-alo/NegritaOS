import React from 'react';

/**
 * Stat — a single metric: label, big mono value, optional unit + delta.
 * The workhorse for ADHD-friendly slides: one number, stated plainly.
 */
export function Stat({
  label,
  value,
  unit = null,
  delta = null,          // e.g. "+1.8%" or "-9ms"
  direction = null,      // 'up' | 'down' | null  (semantic, not arrow direction)
  goodWhen = 'up',       // 'up' | 'down' — which direction is "good" (green)
  size = 'md',           // 'sm' | 'md' | 'lg' | 'xl'
  hint = null,
  style = {},
}) {
  const valSize = { sm: 'var(--text-xl)', md: 'var(--text-2xl)', lg: 'var(--text-4xl)', xl: 'var(--text-5xl)' }[size];
  const good = direction === goodWhen;
  const deltaColor = direction == null ? 'var(--text-muted)' : (good ? 'var(--pos)' : 'var(--neg)');
  const arrow = direction === 'up' ? '▲' : direction === 'down' ? '▼' : '';
  return (
    <div style={style}>
      <div style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', letterSpacing: '0.01em', marginBottom: 8 }}>{label}</div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontWeight: 500, color: 'var(--text-strong)',
          fontSize: valSize, lineHeight: 1, letterSpacing: '-0.01em', fontVariantNumeric: 'tabular-nums',
        }}>{value}</span>
        {unit && <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-md)', color: 'var(--text-muted)' }}>{unit}</span>}
        {delta != null && (
          <span style={{ fontSize: 'var(--text-sm)', fontWeight: 600, color: deltaColor, fontVariantNumeric: 'tabular-nums', display: 'inline-flex', alignItems: 'center', gap: 3 }}>
            {arrow && <span style={{ fontSize: '0.8em' }}>{arrow}</span>}{delta}
          </span>
        )}
      </div>
      {hint && <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-subtle)', marginTop: 6 }}>{hint}</div>}
    </div>
  );
}
