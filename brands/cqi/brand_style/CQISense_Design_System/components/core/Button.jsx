import React from 'react';

/**
 * CQISense Button — bold, confident, cobalt-first.
 * Variants: primary (cobalt fill), secondary (outline), ghost, danger.
 * Sizes: sm | md | lg.
 */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  iconLeft = null,
  iconRight = null,
  disabled = false,
  full = false,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: { height: 'var(--control-sm)', padding: '0 12px', font: 'var(--text-sm)', radius: 'var(--radius-sm)', gap: '6px' },
    md: { height: 'var(--control-md)', padding: '0 16px', font: 'var(--text-sm)', radius: 'var(--radius-md)', gap: '8px' },
    lg: { height: 'var(--control-lg)', padding: '0 22px', font: 'var(--text-md)', radius: 'var(--radius-md)', gap: '9px' },
  }[size];

  const variants = {
    primary: { background: 'var(--brand)', color: 'var(--on-brand)', border: '1px solid var(--brand)' },
    secondary: { background: 'var(--surface-card)', color: 'var(--text-strong)', border: '1px solid var(--border-strong)' },
    ghost: { background: 'transparent', color: 'var(--text-body)', border: '1px solid transparent' },
    danger: { background: 'var(--danger)', color: 'var(--text-inverse)', border: '1px solid var(--danger)' },
  }[variant];

  const [hover, setHover] = React.useState(false);
  const hoverBg = {
    primary: 'var(--brand-hover)',
    secondary: 'var(--gray-100)',
    ghost: 'var(--gray-100)',
    danger: 'var(--pink-500)',
  }[variant];

  return (
    <button
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        gap: sizes.gap, height: sizes.height, padding: sizes.padding,
        width: full ? '100%' : 'auto',
        fontFamily: 'var(--font-body)', fontSize: sizes.font, fontWeight: 'var(--weight-semibold)',
        letterSpacing: '0.01em', lineHeight: 1, whiteSpace: 'nowrap',
        borderRadius: sizes.radius, cursor: disabled ? 'not-allowed' : 'pointer',
        transition: 'background var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out)',
        opacity: disabled ? 0.45 : 1,
        transform: hover && !disabled ? 'translateY(-1px)' : 'none',
        ...variants,
        ...(hover && !disabled ? { background: hoverBg, borderColor: hoverBg } : null),
        ...(variant === 'secondary' && hover && !disabled ? { borderColor: 'var(--border-strong)', background: 'var(--gray-100)' } : null),
        ...style,
      }}
      {...rest}
    >
      {iconLeft}{children}{iconRight}
    </button>
  );
}
