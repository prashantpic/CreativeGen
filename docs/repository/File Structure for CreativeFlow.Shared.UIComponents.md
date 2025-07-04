# Specification

# 1. Files

- **Path:** package.json  
**Description:** Root package.json for the monorepo. Manages workspaces (React, Flutter, design-tokens), development dependencies (Lerna/Turborepo, Storybook, ESLint, Prettier), and root-level scripts to build, test, and lint all packages.  
**Template:** Node.js package.json  
**Dependency Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Monorepo
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Monorepo Workspace Management
    - Root Scripting
    
**Requirement Ids:**
    
    
**Purpose:** Defines the monorepo structure and provides centralized script execution for managing the design system's multiple packages.  
**Logic Description:** Configure workspaces to point to 'packages/*'. Add scripts for 'bootstrap', 'build', 'test', 'storybook', and 'lint' that use the monorepo tool (e.g., Lerna, Turborepo) to run the corresponding command in each package. Include shared dev dependencies like TypeScript, ESLint, Prettier, and Storybook.  
**Documentation:**
    
    - **Summary:** Manages project-wide dependencies and scripts, orchestrating the build and development processes for the shared React, Flutter, and design token packages.
    
**Namespace:** CreativeFlow.Shared.UI  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** lerna.json  
**Description:** Configuration file for the Lerna monorepo manager. Defines the versioning strategy (independent or fixed), npm client, and location of the packages.  
**Template:** Lerna Configuration  
**Dependency Level:** 0  
**Name:** lerna  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Monorepo
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Monorepo Versioning Strategy
    - Package Management Configuration
    
**Requirement Ids:**
    
    
**Purpose:** To configure the behavior of the Lerna monorepo tool for managing inter-package dependencies and versioning.  
**Logic Description:** Set 'packages' to ['packages/*']. Define the 'version' strategy, typically 'independent' for a component library. Specify the 'npmClient' to be used, like 'npm' or 'yarn'.  
**Documentation:**
    
    - **Summary:** Lerna configuration file that orchestrates versioning and dependency management across the different packages within this shared UI components repository.
    
**Namespace:** CreativeFlow.Shared.UI  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** .storybook/main.js  
**Description:** Main Storybook configuration file. Configures addons (e.g., a11y, controls, actions), specifies the location of story files, and customizes the underlying Webpack/Vite configuration for Storybook's manager and preview environments. Primarily for the React components.  
**Template:** Storybook Configuration  
**Dependency Level:** 1  
**Name:** main  
**Type:** Configuration  
**Relative Path:** .storybook  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Component-Driven Development
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Storybook Setup
    - Component Showcase Configuration
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To configure the Storybook development environment for visualizing and interactively testing React UI components in isolation.  
**Logic Description:** Point 'stories' to the source files within the 'packages/react-components/src/**/*.stories.@(js|jsx|ts|tsx)' pattern. Register essential addons like '@storybook/addon-links', '@storybook/addon-essentials', and '@storybook/addon-a11y' for accessibility testing. Configure any necessary Webpack or Vite resolvers to handle monorepo paths.  
**Documentation:**
    
    - **Summary:** Configures the Storybook instance, defining where to find component stories and which addons to enable for a rich development and documentation experience.
    
**Namespace:** CreativeFlow.Shared.UI.Storybook  
**Metadata:**
    
    - **Category:** Tooling
    
- **Path:** .storybook/preview.js  
**Description:** Storybook preview configuration. Sets global parameters, decorators, and provides a theme context (if applicable) to all stories. Useful for wrapping all components in a theme provider or global style resets.  
**Template:** Storybook Configuration  
**Dependency Level:** 1  
**Name:** preview  
**Type:** Configuration  
**Relative Path:** .storybook  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Component-Driven Development
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Global Story Decorators
    - Theme Application in Storybook
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To configure the global rendering of all stories, allowing for consistent theming and layout in the Storybook UI.  
**Logic Description:** Export a 'parameters' object to configure global settings like 'actions' and 'controls'. Export a 'decorators' array to wrap every story in global providers, such as a Styled Components ThemeProvider, to ensure components render with the correct theme.  
**Documentation:**
    
    - **Summary:** Defines the global canvas for all Storybook stories, enabling consistent theming, background settings, and other preview-level configurations.
    
**Namespace:** CreativeFlow.Shared.UI.Storybook  
**Metadata:**
    
    - **Category:** Tooling
    
- **Path:** packages/design-tokens/package.json  
**Description:** Package definition for the design tokens package. Manages dependencies like 'style-dictionary' and defines build scripts to transform platform-agnostic tokens into platform-specific outputs (CSS, SCSS, Dart).  
**Template:** Node.js package.json  
**Dependency Level:** 1  
**Name:** package  
**Type:** Configuration  
**Relative Path:** packages/design-tokens  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Design Tokens
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Design Token Management
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To manage the dependencies and scripts for the design tokens sub-package, which is the source of truth for the design system.  
**Logic Description:** Define the package name (e.g., '@creativeflow/design-tokens'). Add 'style-dictionary' as a dev dependency. Create a 'build' script that executes the Style Dictionary CLI or a custom build script (e.g., 'node build.js').  
**Documentation:**
    
    - **Summary:** Defines the design tokens package, its dependencies, and the scripts needed to compile raw token files into usable formats for both web and mobile platforms.
    
**Namespace:** CreativeFlow.Shared.UI.Tokens  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** packages/design-tokens/config.json  
**Description:** Configuration file for the Style Dictionary build process. Defines the source token files and the output platforms (e.g., CSS variables, SCSS variables, Dart/Flutter theme files), specifying transforms and file formats for each.  
**Template:** JSON Configuration  
**Dependency Level:** 2  
**Name:** config  
**Type:** Configuration  
**Relative Path:** packages/design-tokens  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Design Tokens
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Token Transformation Rules
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To instruct the Style Dictionary tool on how to parse source token files and what format to output them in for different platforms.  
**Logic Description:** Define the 'source' array pointing to 'tokens/**/*.json'. Define a 'platforms' object with keys like 'css', 'scss', and 'dart'. For each platform, specify the 'transformGroup', 'buildPath', and 'files' array. The 'files' array will define the destination file, format (e.g., 'css/variables', 'flutter/class.dart'), and any specific options or filters.  
**Documentation:**
    
    - **Summary:** The core configuration for Style Dictionary, defining the input token files and the output formats and locations for each target platform (web, mobile).
    
**Namespace:** CreativeFlow.Shared.UI.Tokens  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** packages/design-tokens/tokens/color/base.json  
**Description:** Source of truth for all color tokens in the design system. Uses a structured JSON format that Style Dictionary can parse. Defines the entire color palette.  
**Template:** JSON Data  
**Dependency Level:** 1  
**Name:** base.color  
**Type:** Data  
**Relative Path:** packages/design-tokens/tokens/color  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Design Tokens
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Color Token Definition
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To provide a single, platform-agnostic source for all color values used in the design system.  
**Logic Description:** Structure the JSON with a top-level 'color' key. Inside, create categories like 'primary', 'secondary', 'neutral', 'feedback'. Under each category, define specific color values with names (e.g., 'blue-500') and their hex, rgba, or hsl values. This structure allows for systematic generation of theme files.  
**Documentation:**
    
    - **Summary:** Contains the raw definitions for the application's color palette, acting as the single source of truth for all color-related design decisions.
    
**Namespace:** CreativeFlow.Shared.UI.Tokens.Color  
**Metadata:**
    
    - **Category:** Data
    
- **Path:** packages/design-tokens/tokens/size/spacing.json  
**Description:** Source of truth for all spacing and sizing tokens (e.g., padding, margin, border-radius, widths, heights).  
**Template:** JSON Data  
**Dependency Level:** 1  
**Name:** spacing.size  
**Type:** Data  
**Relative Path:** packages/design-tokens/tokens/size  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Design Tokens
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Spacing Token Definition
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To provide a single, platform-agnostic source for all spacing and sizing values to ensure layout consistency.  
**Logic Description:** Structure the JSON with a top-level 'size' key. Inside, categorize tokens like 'spacing', 'borderRadius', 'iconSize'. Use a T-shirt sizing scale (e.g., 'xs', 'sm', 'md', 'lg', 'xl') or a numeric scale to define values in a consistent unit (e.g., 'rem' for web, logical pixels for mobile).  
**Documentation:**
    
    - **Summary:** Contains the raw definitions for the application's spatial system, including spacing, padding, and border radii values.
    
**Namespace:** CreativeFlow.Shared.UI.Tokens.Size  
**Metadata:**
    
    - **Category:** Data
    
- **Path:** packages/react-components/package.json  
**Description:** Package definition for the React component library. Defines the package name, version, dependencies (e.g., React, styled-components), peer dependencies, and build scripts.  
**Template:** Node.js package.json  
**Dependency Level:** 2  
**Name:** package.react  
**Type:** Configuration  
**Relative Path:** packages/react-components  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - React Component Library Definition
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To manage the dependencies, metadata, and build process for the consumable React component library package.  
**Logic Description:** Set the package 'name' to '@creativeflow/react-ui'. Specify 'react' and 'react-dom' as 'peerDependencies'. Add 'styled-components' as a regular dependency. Add dependencies to '@creativeflow/design-tokens'. Define 'main', 'module', and 'types' fields pointing to the build output in the 'dist' folder. The 'build' script will use a bundler like Rollup or Vite.  
**Documentation:**
    
    - **Summary:** The package manifest for the React component library, specifying its dependencies and how it should be consumed by other projects.
    
**Namespace:** CreativeFlow.Shared.UI.React  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** packages/react-components/src/index.ts  
**Description:** Main entry point for the React component library. This file exports all the public components, hooks, and utilities that should be available to consuming applications.  
**Template:** TypeScript Module  
**Dependency Level:** 4  
**Name:** index.react  
**Type:** Module  
**Relative Path:** packages/react-components/src  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Facade Pattern
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Public API Export
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To define the public API of the React component library, acting as a single, consistent entry point for consumers.  
**Logic Description:** Use 'export * from ...' or 'export { default as ComponentName } from ...' statements to re-export every public component from its respective directory (e.g., './components/Button'). Also export any shared hooks or theme providers.  
**Documentation:**
    
    - **Summary:** The public interface of the React component library, exporting all available components, hooks, and utilities for consumption.
    
**Namespace:** CreativeFlow.Shared.UI.React  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** packages/react-components/src/components/Button/Button.tsx  
**Description:** The core logic and JSX for the shared Button component. It accepts props for different variants (primary, secondary, text), sizes, states (disabled, loading), and an onClick handler. Implements accessibility best practices.  
**Template:** React Component (TypeScript)  
**Dependency Level:** 3  
**Name:** Button  
**Type:** Component  
**Relative Path:** packages/react-components/src/components/Button  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Atomic Design (Atom)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Button Component
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    - UI-001 (Modern dashboard - implies shared components)
    
**Purpose:** To provide a consistent, reusable, and accessible button element for all web applications.  
**Logic Description:** Define the component to accept props like 'variant', 'size', 'disabled', 'loading', and 'children'. Render a native '<button>' element. Use styled-components for styling, passing props to the style definition to handle variants. Implement ARIA attributes for accessibility, such as 'aria-disabled'. Show a spinner icon when the 'loading' prop is true.  
**Documentation:**
    
    - **Summary:** A versatile and accessible button component with multiple style variants and states, serving as a fundamental interactive element in the design system.
    
**Namespace:** CreativeFlow.Shared.UI.React.Components  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** packages/react-components/src/components/Button/Button.stories.tsx  
**Description:** Storybook stories for the Button component. Provides interactive examples of all variants, sizes, and states (primary, secondary, disabled, loading) for development and documentation purposes.  
**Template:** Storybook Story (TypeScript)  
**Dependency Level:** 4  
**Name:** Button.stories  
**Type:** Documentation  
**Relative Path:** packages/react-components/src/components/Button  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Component-Driven Development
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Component Showcase
    - Interactive Documentation
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To document and visualize the Button component's different states and props in an isolated, interactive environment.  
**Logic Description:** Import the Button component. Define a default export with the component's 'title' and 'component' metadata. Create named exports for each story, such as 'Primary', 'Secondary', 'Disabled'. Use the 'args' property to set the props for each story variant.  
**Documentation:**
    
    - **Summary:** Provides a live, interactive playground and documentation for the Button component, showcasing its various appearances and functionalities.
    
**Namespace:** CreativeFlow.Shared.UI.React.Stories  
**Metadata:**
    
    - **Category:** Tooling
    
- **Path:** packages/flutter-components/pubspec.yaml  
**Description:** The package definition file for the Flutter component library. Declares the package name, description, version, dependencies (e.g., flutter_svg), and assets (e.g., fonts, icons).  
**Template:** Flutter pubspec  
**Dependency Level:** 2  
**Name:** pubspec  
**Type:** Configuration  
**Relative Path:** packages/flutter-components  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Flutter Package Definition
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To manage the dependencies, metadata, and assets for the consumable Flutter UI component library.  
**Logic Description:** Set the 'name' to 'creative_flow_ui'. Add dependencies like 'flutter_svg' for icon handling. Define the 'flutter' section to include asset paths for fonts (from 'assets/fonts') and icons (from 'assets/icons'). Specify a version number following semantic versioning.  
**Documentation:**
    
    - **Summary:** The manifest for the Flutter UI library, defining its dependencies, assets, and other essential package information for use in Flutter projects.
    
**Namespace:** CreativeFlow.Shared.UI.Flutter  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** packages/flutter-components/lib/creative_flow_ui.dart  
**Description:** Main library file for the Flutter UI package. This file exports all public widgets, theme data, and utilities to be consumed by the main Flutter application.  
**Template:** Dart Library  
**Dependency Level:** 4  
**Name:** creative_flow_ui  
**Type:** Module  
**Relative Path:** packages/flutter-components/lib  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Facade Pattern
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Public API Export (Dart)
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To define the public API of the Flutter widget library, providing a single point of import for consuming applications.  
**Logic Description:** Use 'export' directives to expose all necessary files. For example, 'export 'src/widgets/button/cf_button.dart';', 'export 'src/theme/app_theme.dart';', etc. This ensures consumers only need to import this one file to access the entire library.  
**Documentation:**
    
    - **Summary:** The main entry point for the Flutter component library, which exports all public widgets and theme definitions for use in other Flutter apps.
    
**Namespace:** CreativeFlow.Shared.UI.Flutter  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** packages/flutter-components/lib/src/theme/app_theme.dart  
**Description:** Defines the main ThemeData for the Flutter application. It consumes the generated design token files (color_palette.dart, text_styles.dart) to create a consistent, themeable style for all widgets.  
**Template:** Dart Class  
**Dependency Level:** 3  
**Name:** AppTheme  
**Type:** Theme  
**Relative Path:** packages/flutter-components/lib/src/theme  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Design Tokens
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Flutter Theming
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To provide a centralized ThemeData object that ensures all Flutter widgets in the consuming app adhere to the design system.  
**Logic Description:** Import the generated token files. Create a static method or class that returns a `ThemeData` object. Populate the `ThemeData` properties like `colorScheme`, `textTheme`, `elevatedButtonTheme`, `inputDecorationTheme`, etc., using the constants defined in the imported token files. This centralizes all styling decisions.  
**Documentation:**
    
    - **Summary:** Constructs the Flutter ThemeData object by applying the design tokens, providing a consistent and centralized theme for the mobile application.
    
**Namespace:** CreativeFlow.Shared.UI.Flutter.Theme  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** packages/flutter-components/lib/src/widgets/button/cf_button.dart  
**Description:** The core logic and implementation for the shared Flutter Button widget. It is a stateless or stateful widget that mirrors the variants and states of its React counterpart (primary, secondary, disabled, loading).  
**Template:** Flutter Widget  
**Dependency Level:** 3  
**Name:** CfButton  
**Type:** Component  
**Relative Path:** packages/flutter-components/lib/src/widgets/button  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    - Atomic Design (Atom)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Flutter Button
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    - UI-001 (Modern dashboard - implies shared components)
    
**Purpose:** To provide a consistent, reusable button widget for all Flutter applications, ensuring visual and behavioral consistency with the web.  
**Logic Description:** Create a StatelessWidget. Define constructor parameters for the button's text, onPressed callback, variant, size, and loading state. In the build method, return an `ElevatedButton`, `TextButton`, or other appropriate button type. Use `Theme.of(context)` to retrieve styles from `app_theme.dart` to apply the correct styling based on the props. Show a `CircularProgressIndicator` if in the loading state.  
**Documentation:**
    
    - **Summary:** A versatile and themeable button widget for Flutter, offering multiple style variants and states to be used across the mobile application.
    
**Namespace:** CreativeFlow.Shared.UI.Flutter.Widgets  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** assets/icons/settings.svg  
**Description:** A shared SVG icon for 'settings'. Stored in a platform-agnostic format to be consumed by both the React and Flutter component libraries.  
**Template:** SVG Asset  
**Dependency Level:** 0  
**Name:** settings.svg  
**Type:** Asset  
**Relative Path:** assets/icons  
**Repository Id:** REPO-SHARED-UI-COMPONENTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Iconography
    
**Requirement Ids:**
    
    - NFR-007 (Consistent design language and interaction patterns)
    
**Purpose:** To provide a single, scalable vector graphic for the settings icon, ensuring visual consistency across all platforms.  
**Logic Description:** This is a static asset file containing the XML definition of the vector graphic. It should be optimized for size and cleaned of any unnecessary editor metadata.  
**Documentation:**
    
    - **Summary:** The vector asset for the 'settings' icon, used by both web and mobile component libraries.
    
**Namespace:** CreativeFlow.Shared.UI.Assets.Icons  
**Metadata:**
    
    - **Category:** Asset
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

