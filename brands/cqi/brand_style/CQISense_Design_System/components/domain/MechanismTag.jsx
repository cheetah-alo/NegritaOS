import React from 'react';

/**
 * MechanismTag — the "why" behind a journey (mechanisms can be multiple).
 * Rendered as a quiet outlined tag with a family dot (repair / risk / mixed).
 */
export const MECHANISMS = {
  PROMISE_DEBT_TO_FRICTION:      { label: 'Promise Debt → Friction', family: 'repair' },
  TECHNICAL_REPAIR_FAILURE:      { label: 'Technical Repair Failure', family: 'repair' },
  OPERATIONAL_LOOP:              { label: 'Operational Loop',         family: 'repair' },
  FRICTION_REPAIR_GAP:           { label: 'Friction Repair Gap',      family: 'repair' },
  UNRESOLVED_MULTI_CALL_FATIGUE: { label: 'Unresolved Multi-Call Fatigue', family: 'repair' },
  COMPETITIVE_EXIT_PRESSURE:     { label: 'Competitive Exit Pressure', family: 'risk' },
  BROKEN_PROMISE_EXIT_ESCALATION:{ label: 'Broken Promise + Exit Escalation', family: 'mixed' },
  RESOLVED_LOW_PRESSURE:         { label: 'Resolved Low Pressure',    family: 'relief' },
};

const FAMILY_COLOR = {
  repair: 'var(--repair)',
  risk: 'var(--risk)',
  mixed: 'var(--arch-d2)',
  relief: 'var(--relief)',
};

export function MechanismTag({ id, label, family, size = 'md', style = {} }) {
  const m = id && MECHANISMS[id] ? MECHANISMS[id] : null;
  const text = label ?? (m ? m.label : id);
  const fam = family ?? (m ? m.family : 'repair');
  const color = FAMILY_COLOR[fam] || 'var(--repair)';
  const pad = size === 'sm' ? '4px 9px' : '5px 11px';
  const fz = size === 'sm' ? 'var(--text-xs)' : 'var(--text-sm)';
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 7, padding: pad,
      border: '1px solid var(--border-soft)', borderRadius: 'var(--radius-full)',
      background: 'var(--surface-card)', color: 'var(--text-body)',
      fontFamily: 'var(--font-body)', fontSize: fz, fontWeight: 500, whiteSpace: 'nowrap', ...style,
    }}>
      <span style={{ width: 8, height: 8, borderRadius: '50%', background: color }} />
      {text}
    </span>
  );
}
