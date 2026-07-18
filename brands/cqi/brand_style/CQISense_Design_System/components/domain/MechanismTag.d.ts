import React from 'react';

export type MechanismId =
  | 'PROMISE_DEBT_TO_FRICTION' | 'TECHNICAL_REPAIR_FAILURE' | 'OPERATIONAL_LOOP'
  | 'FRICTION_REPAIR_GAP' | 'UNRESOLVED_MULTI_CALL_FATIGUE'
  | 'COMPETITIVE_EXIT_PRESSURE' | 'BROKEN_PROMISE_EXIT_ESCALATION' | 'RESOLVED_LOW_PRESSURE';

export type MechanismFamily = 'repair' | 'risk' | 'mixed' | 'relief';

export interface MechanismTagProps {
  /** Known mechanism id — fills label + family automatically. */
  id?: MechanismId;
  /** Override / custom label. */
  label?: string;
  /** Override family (controls the dot color). */
  family?: MechanismFamily;
  size?: 'sm' | 'md';
  style?: React.CSSProperties;
}

export declare const MECHANISMS: Record<MechanismId, { label: string; family: MechanismFamily }>;

/** The "why" behind a journey. Multiple mechanisms can apply. */
export function MechanismTag(props: MechanismTagProps): JSX.Element;
