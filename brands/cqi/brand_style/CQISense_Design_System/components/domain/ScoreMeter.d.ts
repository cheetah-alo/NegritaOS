import React from 'react';

export interface ScoreMeterProps {
  /** Current score (0..max). */
  value: number;
  /** Which pressure family — sets color + default label. Default 'operational'. */
  family?: 'repair' | 'risk' | 'operational';
  /** Override the label. */
  label?: string | null;
  /** Optional threshold marker (e.g. 55 promotion line). */
  threshold?: number | null;
  /** Caption above the threshold marker. */
  thresholdLabel?: string | null;
  /** Scale max. Default 100. */
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  style?: React.CSSProperties;
}

/**
 * 0–100 pressure score as a calm horizontal meter with a big mono value.
 * @startingPoint section="Domain" subtitle="Score meters — Repair / Risk / Operational" viewport="700x220"
 */
export function ScoreMeter(props: ScoreMeterProps): JSX.Element;
