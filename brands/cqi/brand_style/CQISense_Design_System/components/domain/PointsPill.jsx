import React from 'react';

/**
 * PointsPill — a scoring contribution like "+25" or a channel split
 * "TSR +8 / CSR +10". Colored by score family (repair / risk / neutral).
 */
export function PointsPill({ value, family = 'repair', size = 'md', style = {} }) {
  const palette = {
    repair: ['var(--repair-soft)', 'var(--repair-text)'],
    risk: ['var(--risk-soft)', 'var(--risk-text)'],
    neutral: ['var(--gray-100)', 'var(--gray-700)'],
    relief: ['var(--green-100)', 'var(--green-800)'],
  }[family] || ['var(--repair-soft)', 'var(--repair-text)'];
  const fz = size === 'sm' ? 'var(--text-xs)' : size === 'lg' ? 'var(--text-md)' : 'var(--text-sm)';
  const pad = size === 'sm' ? '2px 8px' : '3px 10px';
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', padding: pad,
      borderRadius: 'var(--radius-sm)', background: palette[0], color: palette[1],
      fontFamily: 'var(--font-mono)', fontSize: fz, fontWeight: 600,
      fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap', letterSpacing: '0.01em', ...style,
    }}>
      {value}
    </span>
  );
}

/** ChannelSplit — TSR vs CSR point split, the canonical rule weighting display. */
export function ChannelSplit({ tsr, csr, family = 'repair', style = {} }) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, ...style }}>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>TSR</span>
      <PointsPill value={tsr} family={family} size="sm" />
      <span style={{ color: 'var(--border-strong)' }}>/</span>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>CSR</span>
      <PointsPill value={csr} family={family} size="sm" />
    </span>
  );
}
