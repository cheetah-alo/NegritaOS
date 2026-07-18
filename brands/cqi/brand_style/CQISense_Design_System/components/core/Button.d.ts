import React from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual emphasis. Default 'primary'. */
  variant?: ButtonVariant;
  /** Control height. Default 'md'. */
  size?: ButtonSize;
  /** Element rendered before the label (icon). */
  iconLeft?: React.ReactNode;
  /** Element rendered after the label (icon). */
  iconRight?: React.ReactNode;
  /** Stretch to fill container width. */
  full?: boolean;
  disabled?: boolean;
}

/**
 * Primary action control for CQISense. Use one primary button per view;
 * secondary/ghost for supporting actions.
 *
 * @startingPoint section="Core" subtitle="Buttons — primary, secondary, ghost, danger" viewport="700x150"
 */
export function Button(props: ButtonProps): JSX.Element;
