// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `jsconfig.json` or `tsconfig.json`)
// Learn more at https://github.com/microsoft/TypeScript/wiki/JSDoc-Reference

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'CreativeFlow Developer Platform',
  tagline: 'Build the next generation of creative tools with our powerful APIs.',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://developers.creativeflow.ai',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'CreativeFlow', // Usually your GitHub org/user name.
  projectName: 'developer-portal', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/creativeflow/developer-portal/tree/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/creativeflow/developer-portal/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  plugins: [
    [
      'docusaurus-openapi-docs',
      {
        id: "api",
        config: {
          "developer-platform": {
            specPath: "specs/developer-platform.openapi.yaml", // Path to the OpenAPI spec file
            outputDir: "docs/api/developer-platform", // Output directory for generated docs
            sidebarOptions: {
              groupPathsBy: "tag", // Group endpoints by tag in the sidebar
              categoryLinkSource: "tag",
            },
            // The download URL for the OpenAPI spec
            downloadUrl: "https://developers.creativeflow.ai/specs/developer-platform.openapi.yaml",
          },
          // You can add other microservices here as they get documented
          // "asset-management": {
          //   specPath: "specs/asset-management.openapi.yaml",
          //   outputDir: "docs/api/asset-management",
          // }
        }
      }
    ]
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/creativeflow-social-card.jpg',
      navbar: {
        title: 'CreativeFlow Developers',
        logo: {
          alt: 'CreativeFlow Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Guides',
          },
          {
            to: '/api/developer-platform', // Link to the first page of the API docs
            label: 'API Reference',
            position: 'left',
            activeBaseRegex: `/api/`,
          },
          {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/creativeflow',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Guides',
                to: '/docs/intro',
              },
              {
                label: 'API Reference',
                to: '/api/developer-platform',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/creativeflow',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/creativeflow',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/creativeflow',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/creativeflow',
              },
              {
                label: 'Status',
                href: 'https://status.creativeflow.ai',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} CreativeFlow, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      // Algolia Search Configuration (as specified in SDS)
      algolia: {
        // The application ID provided by Algolia
        appId: 'YOUR_APP_ID',

        // Public API key: it is safe to commit it
        apiKey: 'YOUR_SEARCH_API_KEY',

        indexName: 'creativeflow-developers',

        // Optional: see doc section below
        contextualSearch: true,

        // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
        externalUrlRegex: 'external\\.com|domain\\.com',

        // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: "https://www.some-domain.com/docs"
        replaceSearchResultPathname: {
          from: '/docs/', // or as RegExp: /\/docs\//
          to: '/',
        },

        // Optional: Algolia search parameters
        searchParameters: {},

        // Optional: path for search page that enabled by default (`false` to disable)
        searchPagePath: 'search',
      },
    }),
};

export default config;