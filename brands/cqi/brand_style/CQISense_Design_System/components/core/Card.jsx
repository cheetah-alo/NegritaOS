import React from 'react';

/**
 * Card — the base surface. Paper-flat by default (hairline border),
 * optional soft elevation, optional accent rail on the left edge.
 */
export function Card({
  children,
  elevation = 'flat',     // 'flat' | 'raised' | 'floating'
  accent = null,          // CSS color for a 3px left rail (e.g. 'var(--repair)')
  pad = 'md',             // 'none' | 'sm' | 'md' | 'lg'
  style = {},
  ...rest
}) {
  const shadow = { flat: 'none', raised: 'var(--shadow-sm)', floating: 'var(--shadow-lg)' }[elevation];
  const padding = { none: 0, sm: '14px', md: '20px', lg: '28px' }[pad];
  return (
    <div
      style={{
        position: 'relative',
        background: 'var(--surface-card)',
        border: '1px solid var(--border-hair)',
        borderRadius: 'var(--radius-md)',
        boxShadow: shadow,
        padding,
        overflow: 'hidden',
        ...style,
      }}
      {...rest}
    >
      {accent && (
        <span style={{
          position: 'absolute', left: 0, top: 0, bottom: 0, width: 3,
          background: accent, borderRadius: '3px 0 0 3px',
        }} />
      )}
      {children}
    </div>
  );
}

/** Optional card header: eyebrow + title + right-aligned actions. */
export function CardHeader({ eyebrow, title, actions = null, style = {} }) {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16, marginBottom: 16, ...style }}>
      <div>
        {eyebrow && (
          <div style={{
            fontFamily: 'var(--font-mono)', fontSize: 'var(--text-xs)', fontWeight: 500,
            textTransform: 'uppercase', letterSpacing: 'var(--tracking-caps)', color: 'var(--text-muted)', marginBottom: 5,
          }}>{eyebrow}</div>
        )}
        {title && (
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-xl)', fontWeight: 600, color: 'var(--text-strong)', letterSpacing: 'var(--tracking-snug)' }}>{title}</div>
        )}
      </div>
      {actions}
    </div>
  );
}
