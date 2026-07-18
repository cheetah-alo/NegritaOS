import React from 'react';

/**
 * Badge — small status/label chip. Soft (tinted) or solid fill.
 * tone: neutral | brand | repair | risk | success | warning | danger | info | heat
 */
const TONES = {
  neutral: { soft: ['var(--gray-100)', 'var(--text-body)'], solid: ['var(--gray-700)', 'var(--text-inverse)'] },
  brand:   { soft: ['var(--brand-soft)', 'var(--brand-hover)'], solid: ['var(--brand)', 'var(--on-brand)'] },
  repair:  { soft: ['var(--repair-soft)', 'var(--repair-text)'], solid: ['var(--repair)', 'var(--white)'] },
  risk:    { soft: ['var(--risk-soft)', 'var(--risk-text)'], solid: ['var(--risk)', 'var(--white)'] },
  success: { soft: ['var(--success-soft)', 'var(--success-text)'], solid: ['var(--success)', 'var(--white)'] },
  warning: { soft: ['var(--warning-soft)', 'var(--warning-text)'], solid: ['var(--warning)', 'var(--white)'] },
  danger:  { soft: ['var(--danger-soft)', 'var(--danger-text)'], solid: ['var(--danger)', 'var(--white)'] },
  info:    { soft: ['var(--info-soft)', 'var(--info-text)'], solid: ['var(--info)', 'var(--white)'] },
  heat:    { soft: ['var(--heat-soft)', 'var(--heat-text)'], solid: ['var(--heat)', 'var(--white)'] },
};

export function Badge({ children, tone = 'neutral', solid = false, dot = false, mono = false, style = {}, ...rest }) {
  const [bg, fg] = TONES[tone] ? TONES[tone][solid ? 'solid' : 'soft'] : TONES.neutral.soft;
  return (
    <span
      style={{
        display: 'inline-flex', alignItems: 'center', gap: '6px',
        padding: '3px 9px', borderRadius: 'var(--radius-full)',
        background: bg, color: fg,
        fontFamily: mono ? 'var(--font-mono)' : 'var(--font-body)',
        fontSize: 'var(--text-xs)', fontWeight: 'var(--weight-semibold)',
        letterSpacing: mono ? '0.02em' : '0.01em', lineHeight: 1.4, whiteSpace: 'nowrap',
        ...style,
      }}
      {...rest}
    >
      {dot && <span style={{ width: 6, height: 6, borderRadius: '50%', background: fg, opacity: 0.8 }} />}
      {children}
    </span>
  );
}
