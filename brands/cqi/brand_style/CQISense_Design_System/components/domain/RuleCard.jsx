import React from 'react';
import { Card } from '../core/Card.jsx';
import { Badge } from '../core/Badge.jsx';
import { ArchetypeBadge } from './ArchetypeBadge.jsx';
import { MechanismTag } from './MechanismTag.jsx';
import { ChannelSplit } from './PointsPill.jsx';

/**
 * RuleCard — the "one-row contract" for an Attr Strict rule (R1..R9):
 * code, title, score family, channel points, mechanism, archetype, support.
 * Composes core + domain primitives.
 */
export function RuleCard({
  code,                  // 'R1'
  title,                 // 'Callback Promise Debt'
  family = 'repair',     // 'repair' | 'risk' | 'priority'
  tsr, csr,              // points per channel
  mechanism,             // mechanism id
  archetype,             // archetype code
  strictCalls = null,    // e.g. '87,626'
  strictShare = null,    // e.g. '62.5%'
  status = 'Proposal',   // rule status
  style = {},
}) {
  const famTone = family === 'risk' ? 'risk' : family === 'priority' ? 'heat' : 'repair';
  const accent = family === 'risk' ? 'var(--risk)' : family === 'priority' ? 'var(--heat)' : 'var(--repair)';
  return (
    <Card accent={accent} pad="md" style={style}>
      {/* header row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>{code}</span>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-lg)', fontWeight: 600, color: 'var(--text-strong)', flex: 1, lineHeight: 1.2 }}>{title}</span>
        <Badge tone={famTone} solid>{family === 'priority' ? 'Priority route' : family[0].toUpperCase() + family.slice(1)}</Badge>
      </div>

      {/* contract grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px 20px' }}>
        <Field label="Points">
          {tsr != null ? <ChannelSplit tsr={tsr} csr={csr} family={famTone} /> : <span style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>0 standalone</span>}
        </Field>
        <Field label="Archetype"><ArchetypeBadge code={archetype} size="sm" /></Field>
        <Field label="Mechanism"><MechanismTag id={mechanism} size="sm" /></Field>
        <Field label="Status"><Badge tone="neutral">{status}</Badge></Field>
      </div>

      {(strictCalls || strictShare) && (
        <div style={{ display: 'flex', gap: 24, marginTop: 16, paddingTop: 14, borderTop: '1px solid var(--border-hair)' }}>
          {strictCalls && <Mini label="Strict calls" value={strictCalls} />}
          {strictShare && <Mini label="Strict share" value={strictShare} />}
        </div>
      )}
    </Card>
  );
}

function Field({ label, children }) {
  return (
    <div>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-2xs)', textTransform: 'uppercase', letterSpacing: 'var(--tracking-caps)', color: 'var(--text-subtle)', marginBottom: 6 }}>{label}</div>
      {children}
    </div>
  );
}
function Mini({ label, value }) {
  return (
    <div>
      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 500, fontSize: 'var(--text-md)', color: 'var(--text-strong)', fontVariantNumeric: 'tabular-nums' }}>{value}</span>
      <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginLeft: 6 }}>{label}</span>
    </div>
  );
}
