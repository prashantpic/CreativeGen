import React, { forwardRef, ButtonHTMLAttributes } from 'react';
import styles from './Button.module.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Defines the visual style of the button.
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger' | 'ghost';
  /**
   * Defines the size of the button.
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';
  /**
   * If `true`, the button will take up the full width of its container.
   * @default false
   */
  fullWidth?: boolean;
  /**
   * Optional icon to be displayed before the button text.
   */
  leftIcon?: React.ReactElement;
  /**
   * Optional icon to be displayed after the button text.
   */
  rightIcon?: React.ReactElement;
}

/**
 * A reusable, accessible, and stylable Button component.
 * It adheres to the atomic design methodology and serves as a fundamental
 * building block for interactive elements across the application.
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      leftIcon,
      rightIcon,
      className = '',
      ...props
    },
    ref
  ) => {
    const classNames = [
      styles.buttonBase,
      styles[variant],
      styles[size],
      fullWidth ? styles.fullWidth : '',
      className,
    ].join(' ').trim();

    return (
      <button ref={ref} className={classNames} {...props}>
        {leftIcon && <span className={styles.iconWrapper}>{leftIcon}</span>}
        {children && <span className={styles.buttonText}>{children}</span>}
        {rightIcon && <span className={styles.iconWrapper}>{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;