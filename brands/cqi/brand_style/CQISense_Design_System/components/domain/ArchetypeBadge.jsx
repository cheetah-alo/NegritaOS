import React from 'react';

/**
 * ArchetypeBadge — the journey-state archetypes (A, B, C, D, D2, E, F).
 * Renders a colored letter token + optional full name. The archetype is
 * always the FINAL, prioritized label for a journey.
 */
export const ARCHETYPES = {
  A:  { name: 'Resolved Low Pressure',        color: 'var(--arch-a)'  },
  B:  { name: 'Operational Loop',             color: 'var(--arch-b)'  },
  C:  { name: 'Repair Failure / Recall Risk', color: 'var(--arch-c)'  },
  D:  { name: 'Exit Risk Proximity',          color: 'var(--arch-d)'  },
  D2: { name: 'Broken Promise + Exit',        color: 'var(--arch-d2)' },
  E:  { name: 'Silent Failure / Gap',         color: 'var(--arch-e)'  },
  F:  { name: 'Uncertain Review',             color: 'var(--arch-f)'  },
};

export function ArchetypeBadge({ code = 'C', showName = true, size = 'md', style = {} }) {
  const a = ARCHETYPES[code] || ARCHETYPES.C;
  const dim = { sm: 22, md: 28, lg: 38 }[size];
  const fz = { sm: 'var(--text-xs)', md: 'var(--text-sm)', lg: 'var(--text-lg)' }[size];
  const nameFz = { sm: 'var(--text-xs)', md: 'var(--text-sm)', lg: 'var(--text-md)' }[size];
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10, ...style }}>
      <span style={{
        width: dim, height: dim, minWidth: dim, borderRadius: 'var(--radius-sm)',
        background: a.color, color: 'var(--white)',
        display: 'grid', placeItems: 'center',
        fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: fz, letterSpacing: '-0.01em',
        boxShadow: 'var(--shadow-xs)',
      }}>{code}</span>
      {showName && (
        <span style={{ fontFamily: 'var(--font-body)', fontSize: nameFz, fontWeight: 600, color: 'var(--text-strong)', lineHeight: 1.2 }}>
          {a.name}
        </span>
      )}
    </span>
  );
}
