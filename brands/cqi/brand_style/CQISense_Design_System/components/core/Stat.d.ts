import React from 'react';

export interface StatProps {
  /** Caption above the number. */
  label: string;
  /** The value — string or number (rendered in tabular mono). */
  value: string | number;
  /** Trailing unit (e.g. "%", "ms", "accounts"). */
  unit?: string | null;
  /** Change indicator text, e.g. "+1.8%". */
  delta?: string | null;
  /** Semantic movement of the metric. */
  direction?: 'up' | 'down' | null;
  /** Which direction is "good" (renders green). Default 'up'. */
  goodWhen?: 'up' | 'down';
  /** Value size. Default 'md'. Use 'lg'/'xl' for slides. */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Small footnote under the value. */
  hint?: string | null;
  style?: React.CSSProperties;
}

/**
 * Single metric display — label, big mono value, optional delta.
 * @startingPoint section="Data" subtitle="Stat — one number, stated plainly" viewport="700x150"
 */
export function Stat(props: StatProps): JSX.Element;
