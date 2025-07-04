```typescript
import type { Meta, StoryObj } from '@storybook/react';
import Button from './Button';

/**
 * The Button component is a core interactive element used for actions in forms, dialogs, and more.
 * It comes in different variants and sizes to suit various contexts.
 */
const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'text'],
      description: 'The visual style of the button.',
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
      description: 'The size of the button.',
    },
    loading: {
      control: 'boolean',
      description: 'Shows a loading spinner and disables the button.',
    },
    disabled: {
      control: 'boolean',
      description: 'Disables the button.',
    },
    children: {
      control: 'text',
      description: 'The content displayed inside the button.',
    },
    onClick: {
      action: 'clicked',
      description: 'Function to call when the button is clicked.',
    },
  },
  args: {
    children: 'Button Text',
    loading: false,
    disabled: false,
    variant: 'primary',
    size: 'md',
  },
};

export default meta;

type Story = StoryObj<typeof Button>;

/**
 * The primary button is used for the main call-to-action on a page.
 */
export const Primary: Story = {
  args: {
    variant: 'primary',
  },
};

/**
 * The secondary button is used for secondary actions that are less prominent.
 */
export const Secondary: Story = {
  args: {
    variant: 'secondary',
  },
};

/**
 * The text button is used for the least prominent actions, often in dialogs or cards.
 */
export const Text: Story = {
  args: {
    variant: 'text',
  },
};

/**
 * A large-sized button for emphasized actions.
 */
export const Large: Story = {
  args: {
    size: 'lg',
  },
};

/**
 * A small-sized button for compact UI areas.
 */
export const Small: Story = {
  args: {
    size: 'sm',
  },
};

/**
 * The loading state indicates an action is in progress. The button is disabled.
 */
export const Loading: Story = {
  args: {
    loading: true,
  },
};

/**
 * The disabled state prevents user interaction.
 */
export const Disabled: Story = {
  args: {
    disabled: true,
  },
};
```