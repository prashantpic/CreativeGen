```javascript
/** @type { import('@storybook/react-webpack5').StorybookConfig } */
const config = {
  stories: ['../packages/react-components/src/**/*.mdx', '../packages/react-components/src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-links', 
    '@storybook/addon-essentials', 
    '@storybook/addon-a11y'
  ],
  framework: {
    name: '@storybook/react-webpack5',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  staticDirs: ['../assets'], // Make assets available in Storybook
};
export default config;
```