/**
 * Defines the TypeScript interface for the application's theme.
 * This ensures type safety when accessing theme properties throughout the app.
 */
export interface AppTheme {
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    textPrimary: string;
    textSecondary: string;
    error: string;
    success: string;
    warning: string;
    info: string;
    border: string;
  };
  typography: {
    fontFamily: string;
    fontSizeBase: string;
    h1Size: string;
    h2Size: string;
    h3Size: string;
    h4Size: string;
    pSize: string;
    smallSize: string;
  };
  spacing: {
    xs: string; // 4px
    sm: string; // 8px
    md: string; // 16px
    lg: string; // 24px
    xl: string; // 32px
    xxl: string; // 48px
  };
  breakpoints: {
    sm: string; // 640px
    md: string; // 768px
    lg: string; // 1024px
    xl: string; // 1280px
    xxl: string; // 1536px
  };
  radii: {
    sm: string;
    md: string;
    lg: string;
    full: string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
  };
  zIndex: {
    dropdown: number;
    modal: number;
    tooltip: number;
    notification: number;
  };
}

/**
 * A centralized theme object containing all design tokens for the application.
 * This ensures a consistent visual style across all components.
 * These values can be used with CSS-in-JS libraries or to generate CSS custom properties.
 */
export const defaultTheme: AppTheme = {
  colors: {
    primary: '#6A1B9A', // Purple
    secondary: '#4A148C', // Darker Purple
    accent: '#F50057', // Pink
    background: '#F8F9FA', // Light Gray
    surface: '#FFFFFF', // White
    textPrimary: '#212529', // Almost Black
    textSecondary: '#6C757D', // Gray
    error: '#D32F2F', // Red
    success: '#388E3C', // Green
    warning: '#FBC02D', // Yellow
    info: '#1976D2', // Blue
    border: '#DEE2E6',
  },
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    fontSizeBase: '16px',
    h1Size: '2.5rem',
    h2Size: '2rem',
    h3Size: '1.75rem',
    h4Size: '1.5rem',
    pSize: '1rem',
    smallSize: '0.875rem',
  },
  spacing: {
    xs: '0.25rem', // 4px
    sm: '0.5rem',  // 8px
    md: '1rem',    // 16px
    lg: '1.5rem',  // 24px
    xl: '2rem',    // 32px
    xxl: '3rem',   // 48px
  },
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    xxl: '1536px',
  },
  radii: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '1rem',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  },
  zIndex: {
    dropdown: 1000,
    modal: 1050,
    tooltip: 1100,
    notification: 1200,
  }
};