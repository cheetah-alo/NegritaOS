import React from 'react';
import { ArchetypeCode } from './ArchetypeBadge';
import { MechanismId } from './MechanismTag';

export interface RuleCardProps {
  /** Rule code, e.g. "R1". */
  code: string;
  /** Business name, e.g. "Callback Promise Debt". */
  title: string;
  /** Score family — sets accent + family badge. Default 'repair'. */
  family?: 'repair' | 'risk' | 'priority';
  /** TSR channel points, e.g. "+8". Omit for a priority-route rule. */
  tsr?: string | number;
  /** CSR channel points, e.g. "+10". */
  csr?: string | number;
  /** Mechanism id. */
  mechanism?: MechanismId;
  /** Resulting archetype code. */
  archetype?: ArchetypeCode;
  /** Support — strict call count, e.g. "87,626". */
  strictCalls?: string | null;
  /** Support — strict share, e.g. "62.5%". */
  strictShare?: string | null;
  /** Rule status label. Default 'Proposal'. */
  status?: string;
  style?: React.CSSProperties;
}

/**
 * The one-row contract for an Attr Strict rule (R1–R9): points, mechanism,
 * archetype, support. Composes Card + Badge + ArchetypeBadge + MechanismTag.
 * @startingPoint section="Domain" subtitle="Rule contract card (R1–R9)" viewport="700x320"
 */
export function RuleCard(props: RuleCardProps): JSX.Element;
