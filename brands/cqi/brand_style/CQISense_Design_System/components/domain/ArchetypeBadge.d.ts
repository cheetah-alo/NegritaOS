import React from 'react';

export type ArchetypeCode = 'A' | 'B' | 'C' | 'D' | 'D2' | 'E' | 'F';

export interface ArchetypeBadgeProps {
  /** Archetype code. Default 'C'. */
  code?: ArchetypeCode;
  /** Show the full archetype name beside the token. Default true. */
  showName?: boolean;
  size?: 'sm' | 'md' | 'lg';
  style?: React.CSSProperties;
}

/** Lookup of code -> { name, color }. */
export declare const ARCHETYPES: Record<ArchetypeCode, { name: string; color: string }>;

/**
 * The final, prioritized journey-state label (A–F, D2).
 * @startingPoint section="Domain" subtitle="Archetype badges A–F, D2" viewport="700x180"
 */
export function ArchetypeBadge(props: ArchetypeBadgeProps): JSX.Element;
