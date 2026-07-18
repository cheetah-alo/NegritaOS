import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Shadow depth. Default 'flat' (hairline only). */
  elevation?: 'flat' | 'raised' | 'floating';
  /** CSS color for a 3px accent rail on the left edge. */
  accent?: string | null;
  /** Inner padding. Default 'md'. */
  pad?: 'none' | 'sm' | 'md' | 'lg';
}

export interface CardHeaderProps {
  /** Small uppercase mono label above the title. */
  eyebrow?: string;
  /** Serif title. */
  title?: string;
  /** Right-aligned actions node. */
  actions?: React.ReactNode;
  style?: React.CSSProperties;
}

/**
 * Base surface container.
 * @startingPoint section="Core" subtitle="Card surface — flat, raised, accent rail" viewport="700x200"
 */
export function Card(props: CardProps): JSX.Element;
export function CardHeader(props: CardHeaderProps): JSX.Element;
