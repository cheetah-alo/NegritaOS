import React from 'react';

export type ScoreFamily = 'repair' | 'risk' | 'neutral' | 'relief';

export interface PointsPillProps {
  /** The points text, e.g. "+25" or "0". */
  value: string | number;
  /** Score family — controls color. Default 'repair'. */
  family?: ScoreFamily;
  size?: 'sm' | 'md' | 'lg';
  style?: React.CSSProperties;
}

export interface ChannelSplitProps {
  /** TSR points, e.g. "+8". */
  tsr: string | number;
  /** CSR points, e.g. "+10". */
  csr: string | number;
  family?: ScoreFamily;
  style?: React.CSSProperties;
}

/** A scoring contribution (e.g. "+25"), colored by family. */
export function PointsPill(props: PointsPillProps): JSX.Element;
/** TSR / CSR point split — the canonical per-rule channel weighting. */
export function ChannelSplit(props: ChannelSplitProps): JSX.Element;
