import React from 'react';

/**
 * ScoreMeter — a 0-100 pressure score (Repair / Risk / Operational) shown as
 * a calm horizontal meter with a big mono value. Optional threshold marker
 * (e.g. the >=55 archetype-promotion line).
 */
const FAMILY = {
  repair: { track: 'var(--repair-soft)', fill: 'var(--repair)', text: 'var(--repair-text)', label: 'Repair Pressure' },
  risk: { track: 'var(--risk-soft)', fill: 'var(--risk)', text: 'var(--risk-text)', label: 'Risk Pressure' },
  operational: { track: 'var(--operational-soft)', fill: 'var(--operational)', text: 'var(--green-800)', label: 'Operational Score' },
};

export function ScoreMeter({
  value,                 // 0..100
  family = 'operational',
  label = null,          // overrides default family label
  threshold = null,      // 0..100 marker line, e.g. 55
  thresholdLabel = null,
  max = 100,
  size = 'md',           // 'sm' | 'md' | 'lg'
  style = {},
}) {
  const f = FAMILY[family] || FAMILY.operational;
  const pct = Math.max(0, Math.min(100, (value / max) * 100));
  const h = { sm: 8, md: 12, lg: 16 }[size];
  const valFz = { sm: 'var(--text-xl)', md: 'var(--text-2xl)', lg: 'var(--text-4xl)' }[size];
  return (
    <div style={style}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 8 }}>
        <span style={{ fontSize: 'var(--text-sm)', fontWeight: 600, color: 'var(--text-muted)', letterSpacing: '0.01em' }}>{label ?? f.label}</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 500, fontSize: valFz, color: f.text, lineHeight: 1, fontVariantNumeric: 'tabular-nums' }}>
          {value}<span style={{ fontSize: '0.5em', color: 'var(--text-subtle)', marginLeft: 2 }}>/{max}</span>
        </span>
      </div>
      <div style={{ position: 'relative', height: h, borderRadius: 'var(--radius-full)', background: f.track, overflow: 'visible' }}>
        <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: pct + '%', background: f.fill, borderRadius: 'var(--radius-full)', transition: 'width var(--dur-slow) var(--ease-out)' }} />
        {threshold != null && (
          <span style={{ position: 'absolute', left: (threshold / max) * 100 + '%', top: -3, bottom: -3, width: 2, background: 'var(--gray-700)', borderRadius: 2 }}>
            {thresholdLabel && (
              <span style={{ position: 'absolute', top: -18, left: '50%', transform: 'translateX(-50%)', whiteSpace: 'nowrap', fontFamily: 'var(--font-mono)', fontSize: 'var(--text-2xs)', color: 'var(--gray-700)' }}>{thresholdLabel}</span>
            )}
          </span>
        )}
      </div>
    </div>
  );
}
