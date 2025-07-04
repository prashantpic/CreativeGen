```javascript
import React from 'react';
import { ThemeProvider } from 'styled-components';

/**
 * A placeholder theme that mimics the structure of the design tokens.
 * In a real application, you would import the generated theme object.
 * This ensures components render correctly in Storybook even before the
 * design-tokens package has been built.
 */
const placeholderTheme = {
  color: {
    primary: {
      blue: {
        500: { value: '#3B82F6' },
        600: { value: '#2563EB' },
      },
      gray: {
        100: { value: '#F3F4F6' },
      }
    },
    neutral: {
      white: { value: '#FFFFFF' },
      gray: {
        500: { value: '#6B7280' },
        700: { value: '#374151' },
      }
    },
    feedback: {
      blue: {
        100: { value: '#DBEAFE' },
      }
    }
  },
  size: {
    borderRadius: {
      md: { value: '0.375rem' },
      lg: { value: '0.5rem' },
    },
    spacing: {
      '1': { value: '0.25rem' },
      '2': { value: '0.5rem' },
      '3': { value: '0.75rem' },
      '4': { value: '1rem' },
      '6': { value: '1.5rem' },
    },
    icon: {
      md: { value: '1.25rem' }
    }
  }
};


/** @type { import('@storybook/react').Preview } */
const preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  decorators: [
    (Story) => (
      <ThemeProvider theme={placeholderTheme}>
        <Story />
      </ThemeProvider>
    ),
  ],
};

export default preview;
```