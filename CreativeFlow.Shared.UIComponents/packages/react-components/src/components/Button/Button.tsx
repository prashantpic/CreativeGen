```typescript
import React, { forwardRef } from 'react';
import styled, { css } from 'styled-components';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Defines the button's visual style.
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'text';
  /**
   * Defines the button's size.
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';
  /**
   * If `true`, the button will show a loading spinner and be disabled.
   * @default false
   */
  loading?: boolean;
  /**
   * If `true`, the button will be disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The content of the button.
   */
  children: React.ReactNode;
}

const variantStyles = {
  primary: css`
    background-color: ${({ theme }) => theme.color.primary.blue[500].value};
    color: ${({ theme }) => theme.color.neutral.white.value};
    border: 1px solid transparent;

    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.color.primary.blue[600].value};
    }
  `,
  secondary: css`
    background-color: ${({ theme }) => theme.color.neutral.white.value};
    color: ${({ theme }) => theme.color.neutral.gray[700].value};
    border: 1px solid ${({ theme }) => theme.color.neutral.gray[300].value};

    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.color.primary.gray[100].value};
    }
  `,
  text: css`
    background-color: transparent;
    color: ${({ theme }) => theme.color.primary.blue[500].value};
    border: 1px solid transparent;

    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.color.feedback.blue[100].value};
    }
  `,
};

const sizeStyles = {
  sm: css`
    font-size: 0.875rem;
    padding: ${({ theme }) => `${theme.size.spacing[2].value} ${theme.size.spacing[3].value}`};
  `,
  md: css`
    font-size: 1rem;
    padding: ${({ theme }) => `${theme.size.spacing[2].value} ${theme.size.spacing[4].value}`};
  `,
  lg: css`
    font-size: 1.125rem;
    padding: ${({ theme }) => `${theme.size.spacing[3].value} ${theme.size.spacing[6].value}`};
  `,
};

const Spinner = styled.div`
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: currentColor;
  width: 1em;
  height: 1em;
  animation: spin 1s ease-in-out infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const StyledButton = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 500;
  border-radius: ${({ theme }) => theme.size.borderRadius.md.value};
  cursor: pointer;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, border-color 0.2s ease-in-out;
  
  ${({ variant = 'primary' }) => variantStyles[variant]}
  ${({ size = 'md' }) => sizeStyles[size]}

  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
`;

/**
 * A versatile and accessible button component with multiple style variants and states,
 * serving as a fundamental interactive element in the design system.
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { children, variant = 'primary', size = 'md', loading = false, disabled = false, ...props },
    ref
  ) => {
    const isButtonDisabled = loading || disabled;

    return (
      <StyledButton
        ref={ref}
        variant={variant}
        size={size}
        disabled={isButtonDisabled}
        aria-disabled={isButtonDisabled}
        {...props}
      >
        {loading && <Spinner />}
        {children}
      </StyledButton>
    );
  }
);

Button.displayName = 'Button';

export default Button;
```