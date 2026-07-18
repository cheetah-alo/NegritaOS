import React from 'react';

export type BadgeTone =
  | 'neutral' | 'brand' | 'repair' | 'risk'
  | 'success' | 'warning' | 'danger' | 'info' | 'heat';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Semantic color. 'repair'/'risk' map to the score families; 'heat' = Hot Orange priority. Default 'neutral'. */
  tone?: BadgeTone;
  /** Solid fill instead of soft tint. */
  solid?: boolean;
  /** Show a leading status dot. */
  dot?: boolean;
  /** Use the mono font (for codes / IDs / point values). */
  mono?: boolean;
}

/** Small status or label chip. */
export function Badge(props: BadgeProps): JSX.Element;
