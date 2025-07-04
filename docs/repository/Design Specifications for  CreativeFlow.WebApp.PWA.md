# Software Design Specification: CreativeFlow.WebApp.PWA

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the CreativeFlow.WebApp.PWA repository. This Progressive Web Application (PWA) serves as the primary user-facing web interface for the CreativeFlow AI platform. It enables users to manage their accounts, create and manage creative projects, utilize AI-powered content generation tools, collaborate with team members, and interact with various platform services.

### 1.2 Scope
The scope of this document covers the design of the CreativeFlow.WebApp.PWA, including its architecture, components, interfaces, data handling, and PWA-specific features. It details the client-side implementation for:
*   User authentication and account management.
*   Creative asset generation workflows.
*   Workbench, project, and asset management.
*   Brand kit management.
*   Real-time collaboration features (client-side aspects).
*   Subscription and billing information display.
*   Developer portal interactions (API key/webhook management UI).
*   Internationalization and accessibility.
*   Offline capabilities via PWA service workers.

Interaction with backend services will be through a defined API Gateway or Backend-for-Frontend (BFF).

### 1.3 Definitions, Acronyms, and Abbreviations
*   **PWA:** Progressive Web Application
*   **SPA:** Single Page Application
*   **API:** Application Programming Interface
*   **JWT:** JSON Web Token
*   **CRUD:** Create, Read, Update, Delete
*   **WYSIWYG:** What You See Is What You Get
*   **i18n:** Internationalization
*   **a11y:** Accessibility
*   **LCP:** Largest Contentful Paint
*   **FID:** First Input Delay
*   **CLS:** Cumulative Layout Shift
*   **CDN:** Content Delivery Network
*   **CRDT:** Conflict-free Replicated Data Type
*   **TS:** TypeScript
*   **SDK:** Software Development Kit
*   **UGC:** User-Generated Content
*   **MFA:** Multi-Factor Authentication
*   **UI:** User Interface
*   **UX:** User Experience
*   **NFR:** Non-Functional Requirement
*   **SDS:** Software Design Specification
*   **UAPM:** User Account & Profile Management (Requirement Group)
*   **RUM:** Real User Monitoring

### 1.4 References
*   CreativeFlow AI System Requirements Specification (SRS) Document (implicit, based on provided requirements)
*   CreativeFlow AI Architecture Design Document (implicit, based on provided architecture style and patterns)
*   CreativeFlow AI Sequence Diagrams (SD-CF-001 specifically mentioned)
*   React Documentation (react.dev)
*   TypeScript Documentation (typescriptlang.org)
*   Zustand Documentation (docs.pmnd.rs/zustand)
*   React Router Documentation (reactrouter.com)
*   Axios Documentation (axios-http.com)
*   i18next Documentation (i18next.com)
*   Vite Documentation (vitejs.dev)
*   Workbox Documentation (developer.chrome.com/docs/workbox)
*   WCAG 2.1 Guidelines (w3.org/TR/WCAG21/)

### 1.5 Overview
This SDS is organized into sections covering architectural design, data design, interface design, detailed component design, cross-cutting concerns, and specific PWA implementation details. It aims to provide a comprehensive blueprint for the development of the CreativeFlow.WebApp.PWA.

## 2. System Architecture

### 2.1 Architectural Style
The CreativeFlow.WebApp.PWA will be a modern **Single Page Application (SPA)** built with React and TypeScript, designed as a **Progressive Web Application (PWA)**. It will follow a **component-based architecture**, promoting reusability and modularity. While the overall system architecture is "Microservices" and the repository architecture style is "MicroFrontends", this specific PWA will be developed as a cohesive frontend application, which might itself be composed of feature modules that could be considered "micro-frontend-like" in their organization. It primarily serves as the presentation layer for web users.

### 2.2 High-Level Component Diagram (Conceptual)
mermaid
graph TD
    User[Browser/PWA Client] -->|HTTPS| APIGateway[API Gateway / BFF];
    User <--|WebSocket| NotificationService[Notification Service];
    User <--|WebSocket| CollaborationService[Real-time Collaboration Service];

    APIGateway --> AuthSvc[Auth Service];
    APIGateway --> UserProfileSvc[User Profile Service];
    APIGateway --> CreativeSvc[Creative Management Service];
    APIGateway --> AIGenSvc[AI Generation Orchestration];
    APIGateway --> BillingSvc[Subscription & Billing Service];
    APIGateway --> APIDevSvc[API Developer Platform Service];
    APIGateway --> SocialPubSvc[Social Publishing Service];

    subgraph CreativeFlow.WebApp.PWA
        direction LR
        CoreApp[App Core (Router, State, Theme, i18n)]
        AuthModule[Auth Module (Login, Register, MFA)]
        DashboardModule[Dashboard Module]
        EditorModule[Creative Editor Module]
        TemplatesModule[Template Gallery Module]
        ProfileModule[User Profile & Account Module]
        ProjectsModule[Workbench & Projects Module]
        CollabUI[Collaboration UI Components]
        DevPortalUI[Developer Portal UI (Client)]
        PWAFeatures[PWA Features (Service Worker, Offline)]
        SharedUI[Shared UI Components & Hooks]
        APIServices[API Client Services]

        CoreApp --> AuthModule;
        CoreApp --> DashboardModule;
        CoreApp --> EditorModule;
        CoreApp --> TemplatesModule;
        CoreApp --> ProfileModule;
        CoreApp --> ProjectsModule;
        CoreApp --> DevPortalUI;
        CoreApp --> SharedUI;
        CoreApp --> APIServices;
        CoreApp --> PWAFeatures;

        EditorModule --> CollabUI;
    end

    User --> CreativeFlow.WebApp.PWA;
    CreativeFlow.WebApp.PWA --> APIGateway;
    CreativeFlow.WebApp.PWA --> NotificationService;
    CreativeFlow.WebApp.PWA --> CollaborationService;

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style APIGateway fill:#bbf,stroke:#333,stroke-width:2px
    style NotificationService fill:#ccf,stroke:#333,stroke-width:2px
    style CollaborationService fill:#ccf,stroke:#333,stroke-width:2px
    style CreativeFlow.WebApp.PWA fill:#lightgrey,stroke:#333,stroke-width:2px


*This diagram depicts the PWA interacting with backend services via an API Gateway and specialized real-time services. Internally, the PWA is structured into feature modules and shared components.*

### 2.3 Technology Stack
*   **Core Framework:** React 19+
*   **Language:** TypeScript 5.5.3+
*   **Build Tool:** Vite
*   **State Management:** Zustand (primary choice, potential for Redux Toolkit if complex global state scenarios arise demanding its ecosystem)
*   **Routing:** React Router v6+
*   **HTTP Client:** Axios
*   **Internationalization (i18n):** i18next
*   **PWA:** Service Workers (Workbox or custom), Web App Manifest
*   **Styling:** CSS Modules, CSS-in-JS (e.g., Emotion/Styled Components), or Tailwind CSS (To be decided based on team preference for DX and maintainability, leaning towards CSS Modules for component encapsulation or Tailwind CSS for utility-first speed). For this SDS, we will assume CSS Modules for component-scoped styling, supplemented by a global style sheet for base styles and theming.
*   **Testing:** Jest, React Testing Library (for unit/integration), Cypress/Playwright (for E2E test setup)
*   **Linting/Formatting:** ESLint, Prettier

### 2.4 Key Architectural Patterns
#### 2.4.1 State Management (Zustand)
*   **Description:** Zustand will be used for managing global and feature-specific state. It offers a simple, unopinionated, and performant approach to state management.
*   **Structure:** Multiple small stores (slices) will be created for different domains (e.g., `authStore`, `userStore`, `editorStore`).
*   **Middleware:** Zustand middleware (e.g., `persist` for local storage, `immer` for immutable updates) will be used as needed.
*   **Requirement Mapping:** REQ-013 (collaboration state), UI-002 (editor state).

#### 2.4.2 Client-Side Routing (React Router)
*   **Description:** React Router v6+ will manage client-side navigation, enabling a SPA experience.
*   **Structure:** Centralized route configuration (`app/router/index.tsx`) defining public, protected, and nested routes. Layout components will be used for consistent page structures.
*   **Requirement Mapping:** NFR-007 (consistent navigation).

#### 2.4.3 API Client (Axios with Interceptors)
*   **Description:** A centralized Axios instance (`services/apiClient.ts`) will handle all HTTP communication with the backend API Gateway.
*   **Interceptors:**
    *   **Request Interceptor:** To automatically attach JWT authentication tokens to outgoing requests.
    *   **Response Interceptor:** For global error handling (e.g., 401 for unauthorized access leading to logout, generic error notifications).
*   **Requirement Mapping:** NFR-001 (API responsiveness implication).

#### 2.4.4 Progressive Web App (Service Workers, Manifest)
*   **Description:** The application will be a PWA, providing offline capabilities, installability, and enhanced performance.
*   **Service Worker (`src/service-worker.ts`):** Workbox (or custom logic) will be used for:
    *   Caching static assets (app shell, JS/CSS bundles, fonts, images) using a cache-first strategy.
    *   Caching API responses for key read-only data using a network-first or stale-while-revalidate strategy.
    *   Basic offline page display.
*   **Web App Manifest (`public/manifest.json`):** Defines app name, icons, start URL, display mode, theme color for installability.
*   **Requirement Mapping:** Section 5.2.1 (Web App Component), REQ-WCI-001.

#### 2.4.5 Internationalization (i18next)
*   **Description:** i18next will be used for translating all user-facing text.
*   **Setup (`src/app/i18n/index.ts`):** Configuration for supported languages, default language, resource loading (e.g., from `public/locales`), language detection.
*   **Usage:** `useTranslation` hook in components, `Trans` component for complex translations.
*   **Requirement Mapping:** UI-006, PLI-001 to PLI-007.

#### 2.4.6 Theming
*   **Description:** A centralized theme configuration (`src/app/theme/index.ts`) will define colors, typography, spacing, and breakpoints.
*   **Implementation:** Could be used with a CSS-in-JS library or to generate CSS custom properties for use with CSS Modules or global styles.
*   **Requirement Mapping:** NFR-007 (consistent design), UI-001.

## 3. Data Design

### 3.1 Client-Side Data Models (Interfaces/Types)
Located primarily in `src/shared/types/`.
*   **`api.d.ts`:** Defines TypeScript interfaces for all expected API request payloads and response DTOs. This ensures type safety when interacting with the backend. Examples:
    *   `UserLoginRequest`, `UserLoginResponse`, `UserRegistrationRequest`
    *   `UserProfile`, `UpdateUserProfileRequest`
    *   `BrandKit`, `CreateBrandKitRequest`
    *   `Project`, `CreateProjectRequest`
    *   `Asset`, `UploadAssetResponse`
    *   `GenerationRequestPayload`, `GenerationStatusResponse`
    *   `SubscriptionDetails`
    *   `ApiErrorResponse`
*   **`domain.d.ts`:** Defines client-side specific models or augmented types derived from API responses, often used within state management or complex components. Examples:
    *   `EditorElement` (for elements on the creative canvas)
    *   `CollaborationState` (local representation of shared editor state)
    *   `NotificationItem`
*   **Type Generation:** Consider using tools like `openapi-typescript-codegen` if backend provides an OpenAPI spec, to auto-generate `api.d.ts`.

### 3.2 Local Storage / IndexedDB Usage (for PWA offline)
*   **Service Worker Cache:** Managed by Workbox/custom service worker for caching:
    *   App shell (HTML, CSS, JS bundles).
    *   Static assets (images, fonts).
    *   Key API GET requests (e.g., user profile, project list, template list - stale-while-revalidate or cache-first).
*   **Local Storage:**
    *   JWT authentication token and refresh token (securely).
    *   User preferences (e.g., selected theme, language preference if not synced immediately).
    *   PWA update prompt status.
*   **IndexedDB (Optional, for more complex offline data):**
    *   If extensive offline editing capabilities beyond simple asset viewing are required for creative projects (not explicitly detailed as a primary PWA offline feature beyond basic read access in REQ-WCI-001), IndexedDB could store project state or minimal asset data.
    *   For basic read access (REQ-WCI-001), service worker caching of API responses might suffice.
    *   Queuing of actions performed offline (e.g., simple text changes, if implemented for offline editing).

### 3.3 State Management Stores (Zustand)
Located in `src/app/store/slices/` (or similar, if adopting a slice-like pattern with Zustand).
*   **`authStore.ts`:**
    *   State: `isAuthenticated: boolean`, `user: UserProfile | null`, `token: string | null`, `loading: boolean`, `error: string | null`, `mfaRequired: boolean`.
    *   Actions: `login()`, `register()`, `logout()`, `verifyEmail()`, `requestPasswordReset()`, `resetPassword()`, `handleMfa()`, `refreshToken()`, `loadUserFromToken()`.
    *   Connected Requirements: REQ-001, UAPM-1-001, UAPM-1-002, UAPM-1-006.
*   **`userProfileStore.ts`:**
    *   State: `profile: UserProfile | null`, `preferences: UserPreferences`, `brandKits: BrandKit[]`, `currentBrandKit: BrandKit | null`, `loading: boolean`, `error: string | null`.
    *   Actions: `fetchUserProfile()`, `updateUserProfile()`, `updateUserPreferences()`, `fetchBrandKits()`, `createBrandKit()`, `updateBrandKit()`, `deleteBrandKit()`, `setDefaultBrandKit()`.
    *   Connected Requirements: REQ-004, UAPM-1-003, UAPM-1-004, UAPM-1-005, UAPM-1-007, UAPM-1-009.
*   **`projectStore.ts`:** (Manages Workbenches, Projects, Assets)
    *   State: `workbenches: Workbench[]`, `currentWorkbench: Workbench | null`, `projects: Project[]`, `currentProject: Project | null`, `assets: Asset[]`, `assetHistory: AssetVersion[]`, `loading: boolean`, `error: string | null`.
    *   Actions: `fetchWorkbenches()`, `createWorkbench()`, `fetchProjects(workbenchId)`, `createProject(workbenchId, projectData)`, `fetchProjectDetails(projectId)`, `uploadAsset(projectId, file)`, `fetchAssets(projectId)`, `fetchAssetHistory(assetId)`, `saveAssetVersion(assetId, data)`.
    *   Connected Requirements: REQ-010, REQ-011, REQ-4-001 to REQ-4-009.
*   **`creativeEditorStore.ts`:**
    *   State: `canvasState: EditorCanvasState` (elements, dimensions, background), `selectedElementId: string | null`, `zoomLevel: number`, `activeTool: string | null`, `aiSuggestions: AISuggestion[]`, `isCollaborating: boolean`, `collaborators: Collaborator[]`, `generationSamples: SamplePreview[]`, `currentGenerationStatus: string`.
    *   Actions: `setCanvasState()`, `addElement()`, `updateElement()`, `deleteElement()`, `setSelectedElement()`, `setZoom()`, `setActiveTool()`, `requestAISuggestions()`, `initiateAIGeneration()`, `updateGenerationSamples()`, `selectSampleForFinal()`, `updateCollaborationState()`.
    *   Connected Requirements: UI-002, REQ-005, REQ-006, REQ-008, REQ-013.
*   **`templateStore.ts`:**
    *   State: `templates: Template[]`, `categories: string[]`, `trendingTemplates: Template[]`, `recommendedTemplates: Template[]`, `userTemplates: Template[]`, `currentFilters: object`, `loading: boolean`, `error: string | null`.
    *   Actions: `fetchTemplates()`, `fetchTemplateCategories()`, `filterTemplates()`, `saveUserTemplate()`, `fetchUserTemplates()`.
    *   Connected Requirements: UI-003, REQ-005, REQ-WCI-010.
*   **`subscriptionStore.ts`:**
    *   State: `subscriptionDetails: SubscriptionDetails | null`, `creditBalance: number | null` (can also be part of userProfileStore), `usageStats: UsageStats | null`, `loading: boolean`, `error: string | null`.
    *   Actions: `fetchSubscriptionDetails()`, `fetchCreditBalance()`, `fetchUsageStats()`, `initiateUpgrade()`, `initiateCancel()`.
    *   Connected Requirements: REQ-004, REQ-014, REQ-015, REQ-6-005, UAPM-1-005.
*   **`notificationStore.ts`:** (For UI notifications/toasts, not to be confused with the backend Notification Service)
    *   State: `notifications: UINotification[]`.
    *   Actions: `addNotification()`, `removeNotification()`.
    *   Connected Requirements: REQ-WCI-008 (feedback for errors).
*   **`developerPortalStore.ts`:**
    *   State: `apiKeys: ApiKey[]`, `webhooks: WebhookConfig[]`, `loading: boolean`, `error: string | null`.
    *   Actions: `fetchApiKeys()`, `createApiKey()`, `revokeApiKey()`, `fetchWebhooks()`, `createWebhook()`, `updateWebhook()`, `deleteWebhook()`.
    *   Connected Requirements: REQ-017, REQ-018, REQ-7-005.

## 4. Interface Design

### 4.1 User Interface (UI) Design Principles
The PWA UI will adhere to the following principles:
#### 4.1.1 Responsiveness (NFR-007)
*   **Mobile-First Approach:** Design and develop for mobile viewports first, then scale up for tablet and desktop.
*   **Fluid Grids & Flexible Images:** Use relative units (%, vw, vh, rem, em) and flexible layouts (Flexbox, CSS Grid).
*   **Media Queries:** Apply breakpoints to adapt layout, typography, and navigation for different screen sizes.
*   **Touch-Friendly Interactions:** Ensure interactive elements are adequately sized and spaced for touch input on smaller screens.
*   **Requirement Mapping:** REQ-WCI-001.

#### 4.1.2 Accessibility (UI-005, REQ-14-001, REQ-WCI-011)
*   **WCAG 2.1 Level AA Compliance:** Target for all components and pages.
*   **Semantic HTML:** Use appropriate HTML5 elements for structure and meaning.
*   **ARIA Attributes:** Use ARIA roles, states, and properties where necessary to enhance accessibility for assistive technologies.
*   **Keyboard Navigation:** All interactive elements must be focusable and operable via keyboard alone, with a logical focus order.
*   **Screen Reader Compatibility:** Test with common screen readers (NVDA, VoiceOver, TalkBack).
*   **Color Contrast:** Ensure sufficient contrast between text and background.
*   **Alternative Text:** Provide descriptive `alt` text for all meaningful images and icons.
*   **Resizable Text & High Contrast Mode:** Support browser/OS settings for font size adjustment and high contrast modes where feasible.

#### 4.1.3 Consistency (NFR-007)
*   **Design Language:** Adhere to a defined style guide for typography, color palettes, iconography, spacing, and component styling (see `src/app/theme/index.ts`).
*   **Interaction Patterns:** Use consistent patterns for common actions (e.g., saving, deleting, navigation).
*   **Terminology:** Use consistent language and terminology across the application (managed via i18next).
*   **Requirement Mapping:** REQ-WCI-003.

#### 4.1.4 Usability (NFR-007, 3-click rule)
*   **Clarity & Intuitiveness:** Design interfaces that are easy to understand and use.
*   **3-Click Rule:** Core functions should be accessible within a maximum of three user interactions from the main dashboard or relevant context.
*   **Feedback:** Provide clear and timely feedback for user actions (success, error, loading states).
*   **Contextual Help & Tooltips:** Integrate help text and tooltips where needed.
*   **Requirement Mapping:** REQ-WCI-003, REQ-WCI-008.

### 4.2 External API Interfaces
#### 4.2.1 Backend API (via API Gateway or BFF)
*   **Protocol:** HTTPS, RESTful or GraphQL (as defined by backend).
*   **Authentication:** JWT Bearer Tokens in Authorization header.
*   **Data Format:** JSON.
*   **Key Endpoints (Consumed by PWA):** (Detailed in `src/app/config/apiEndpoints.ts` and respective service files)
    *   Auth: `/auth/login`, `/auth/register`, `/auth/verify-email`, `/auth/social-login/{provider}`, `/auth/mfa/setup`, `/auth/mfa/verify`, `/auth/password/request-reset`, `/auth/password/reset`.
    *   User Profile: `/users/me`, `/users/me/profile`, `/users/me/preferences`, `/users/me/brand-kits`, `/users/me/data-portability`, `/users/me/consent`.
    *   Workbenches & Projects: `/workbenches`, `/workbenches/{id}/projects`, `/projects/{id}`, `/projects/{id}/assets`.
    *   Assets: `/assets`, `/assets/{id}/versions`.
    *   Templates: `/templates`, `/templates/categories`, `/users/me/templates`.
    *   Creative Generation: `/generate/request`, `/generate/status/{jobId}`, `/generate/samples/{jobId}`.
    *   Subscription & Billing: `/billing/subscription`, `/billing/credits`, `/billing/usage`.
    *   Developer API (for managing user's own keys/webhooks): `/developer/api-keys`, `/developer/webhooks`.
    *   Social Connections: `/social/connect/{platform}`, `/social/connections`.
*   **Error Handling:** Standard HTTP status codes (400, 401, 403, 404, 500). Error responses will include a machine-readable error code and a user-friendly message (to be localized).

#### 4.2.2 WebSocket Interface
*   **Notification Service (`REPO-NOTIFICATION-SERVICE-001`):**
    *   **Purpose:** Receive real-time updates for UI (e.g., AI generation progress, general notifications).
    *   **Protocol:** Secure WebSockets (WSS).
    *   **Endpoint:** Configured via `VITE_NOTIFICATION_SERVICE_WS_URL`.
    *   **Messages:** JSON payloads. Examples:
        *   `{ type: "GENERATION_PROGRESS", data: { jobId: "...", status: "...", progress: 75 } }`
        *   `{ type: "NEW_NOTIFICATION", data: { title: "...", message: "...", link: "..." } }`
*   **Real-time Collaboration Service (`REPO-COLLABORATION-SERVICE-001`):**
    *   **Purpose:** Exchange CRDT updates for collaborative editing.
    *   **Protocol:** Secure WebSockets (WSS).
    *   **Endpoint:** Configured via `VITE_COLLABORATION_SERVICE_WS_URL`.
    *   **Messages:** Yjs-compatible binary or JSON-encoded CRDT updates, presence events. Examples:
        *   `{ type: "CRDT_UPDATE", projectId: "...", update: "..." }`
        *   `{ type: "USER_JOINED", projectId: "...", user: { id: "...", name: "...", cursor: {...} } }`
        *   `{ type: "USER_LEFT", projectId: "...", userId: "..." }`
        *   `{ type: "CURSOR_MOVED", projectId: "...", userId: "...", cursor: {...} }`

## 5. Detailed Design
This section details the design of files and modules outlined in the `file_structure_json` and derived from requirements.

### 5.1 Core Application Setup
#### 5.1.1 `public/index.html`
*   **Purpose:** Main HTML entry point.
*   **Logic:** Basic HTML structure with `<div id="root"></div>`. Links to `manifest.json`, `favicon.ico`, and main JS/CSS bundles (handled by Vite).
*   **Requirement Mapping:** Section 2.1, Section 5.2.1.

#### 5.1.2 `public/manifest.json`
*   **Purpose:** PWA manifest.
*   **Logic:** JSON configuration.
    json
    {
      "short_name": "CreativeFlow",
      "name": "CreativeFlow AI",
      "icons": [
        { "src": "favicon.ico", "sizes": "64x64 32x32 24x24 16x16", "type": "image/x-icon" },
        { "src": "logo192.png", "type": "image/png", "sizes": "192x192" },
        { "src": "logo512.png", "type": "image/png", "sizes": "512x512" }
      ],
      "start_url": ".",
      "display": "standalone",
      "theme_color": "#000000", // Example, define actual theme color
      "background_color": "#ffffff" // Example
    }
    
*   **Requirement Mapping:** Section 5.2.1.

#### 5.1.3 `src/index.tsx`
*   **Purpose:** React application entry point.
*   **Logic:**
    typescript
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import './index.css'; // Global styles
    import { reportWebVitals } from './reportWebVitals';
    import * as serviceWorkerRegistration from './serviceWorkerRegistration';
    import './app/i18n'; // Initialize i18next

    const root = ReactDOM.createRoot(
      document.getElementById('root') as HTMLElement
    );
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );

    serviceWorkerRegistration.register(); // Or use vite-plugin-pwa auto-registration
    reportWebVitals(console.log); // Or send to analytics
    
*   **Requirement Mapping:** Section 2.1.

#### 5.1.4 `src/App.tsx`
*   **Purpose:** Root component, sets up global providers and layout.
*   **Logic:**
    typescript
    import React from 'react';
    import { BrowserRouter } from 'react-router-dom';
    import { I18nextProvider } from 'react-i18next';
    import i18n from './app/i18n';
    import AppRouter from './app/router';
    import { ThemeProvider } from './app/theme/ThemeProvider'; // Assuming a ThemeProvider component
    // import { GlobalStateProvider } from './app/store'; // If using context-based Zustand, or just import stores directly in components

    function App() {
      return (
        <I18nextProvider i18n={i18n}>
          <ThemeProvider> {/* Assuming a ThemeProvider that applies theme (CSS vars or context) */}
            {/* <GlobalStateProvider> If using a single context provider for Zustand stores */}
              <BrowserRouter>
                {/* Consider adding a global layout component here if needed */}
                <AppRouter />
              </BrowserRouter>
            {/* </GlobalStateProvider> */}
          </ThemeProvider>
        </I18nextProvider>
      );
    }
    export default App;
    
*   **Requirement Mapping:** Section 2.1, UI-006, NFR-007.

### 5.2 PWA Implementation
#### 5.2.1 `src/service-worker.ts`
*   **Purpose:** Offline capabilities, caching, background sync (optional), push notifications (client-side handling).
*   **Technology:** Workbox (via `vite-plugin-pwa`) or custom implementation.
*   **Logic:**
    *   **Caching Strategies:**
        *   App Shell (index.html, main JS/CSS chunks, manifest): Cache-first or Stale-While-Revalidate.
        *   Static Assets (images, fonts in `public` or `src/assets`): Cache-first with expiration.
        *   API GET requests (e.g., user profile, project lists, templates): Network-first, falling back to cache, or Stale-While-Revalidate. Cache dynamic data with caution and clear invalidation strategies.
    *   **Offline Fallback:** Serve a generic offline page or cached content for failed network requests.
    *   **Push Notification Listener:** Handle `push` events, display notifications.
    *   **Background Sync (Optional):** If features require queuing actions offline and syncing later.
*   **Key Workbox Modules/Strategies:** `precacheAndRoute`, `registerRoute`, `CacheFirst`, `NetworkFirst`, `StaleWhileRevalidate`, `ExpirationPlugin`.
*   **Requirement Mapping:** Section 5.2.1, REQ-WCI-001.

#### 5.2.2 `src/serviceWorkerRegistration.ts`
*   **Purpose:** Register and manage the service worker lifecycle.
*   **Logic:** As provided in standard React setups or by `vite-plugin-pwa/client` (e.g., `useRegisterSW` hook for update prompts).
*   Handles `navigator.serviceWorker.register()`.
*   Provides callbacks for `onUpdate` (new SW available) and `onSuccess` (SW installed).
*   **Requirement Mapping:** Section 5.2.1.

#### 5.2.3 `src/app/pwa/pwaUpdatePrompt.tsx`
*   **Purpose:** UI component to inform users of available PWA updates.
*   **Logic:**
    *   Uses a hook (e.g., provided by `vite-plugin-pwa`) to detect when `serviceWorkerRegistration.onUpdate` is triggered.
    *   Displays a modal or toast notification with a message (e.g., "A new version is available!") and an "Update" button.
    *   Clicking "Update" triggers the service worker update mechanism (e.g., `updateSW()` from the hook, which typically calls `skipWaiting()` and reloads the page).
*   **Requirement Mapping:** Section 5.2.1.

### 5.3 Routing (`src/app/router/`)
#### 5.3.1 `index.tsx` (AppRouter)
*   **Purpose:** Defines all application routes.
*   **Logic:**
    typescript
    import React, { Suspense, lazy } from 'react';
    import { Routes, Route, Navigate } from 'react-router-dom';
    import ProtectedRoutes from './ProtectedRoutes';
    import PublicLayout from '@/shared/components/layouts/PublicLayout';
    import AppLayout from '@/shared/components/layouts/AppLayout'; // For authenticated users
    import LoadingSpinner from '@/shared/components/molecules/LoadingSpinner'; // Example

    // Lazy load pages
    const LoginPage = lazy(() => import('@/features/auth/pages/LoginPage'));
    const RegisterPage = lazy(() => import('@/features/auth/pages/RegisterPage'));
    // ... other page imports

    const DashboardPage = lazy(() => import('@/features/dashboard/pages/DashboardPage'));
    // ... other protected page imports

    const AppRouter: React.FC = () => {
      return (
        <Suspense fallback={<LoadingSpinner />}> {/* Or a more sophisticated layout skeleton */}
          <Routes>
            <Route element={<PublicLayout />}>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              {/* <Route path="/verify-email" element={<EmailVerificationPage />} /> */}
              {/* <Route path="/reset-password" element={<PasswordResetPage />} /> */}
            </Route>

            <Route element={<ProtectedRoutes />}>
              <Route element={<AppLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                {/* <Route path="/profile" element={<ProfilePage />} /> */}
                {/* <Route path="/editor/:projectId?" element={<CreativeEditorPage />} /> */}
                {/* <Route path="/templates" element={<TemplateGalleryPage />} /> */}
                {/* <Route path="/workbenches" element={<WorkbenchListPage />} /> */}
                {/* <Route path="/workbenches/:workbenchId/projects" element={<ProjectListPage />} /> */}
                {/* <Route path="/developer" element={<DeveloperPortalPage />} /> */}
                {/* ... other protected routes */}
              </Route>
            </Route>
            {/* <Route path="*" element={<NotFoundPage />} /> */}
          </Routes>
        </Suspense>
      );
    };
    export default AppRouter;
    
*   **Requirement Mapping:** NFR-007.

#### 5.3.2 `ProtectedRoutes.tsx`
*   **Purpose:** Guards routes requiring authentication.
*   **Logic:**
    typescript
    import React from 'react';
    import { Navigate, Outlet } from 'react-router-dom';
    import { useAuthStore } from '@/app/store/slices/authStore'; // Assuming Zustand store

    const ProtectedRoutes: React.FC = () => {
      const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
      const token = useAuthStore((state) => state.token); // Or check token directly from local storage if preferred for initial check

      // Add logic to check token validity if needed, beyond just presence
      if (!isAuthenticated && !token) { // Simple check, can be more robust
        return <Navigate to="/login" replace />;
      }
      return <Outlet />; // Renders child routes defined within it
    };
    export default ProtectedRoutes;
    
*   **Requirement Mapping:** REQ-001.

### 5.4 State Management (`src/app/store/`)
Zustand will be used. Stores will be defined in `src/app/store/slices/` or a similar structure.
Example: `src/app/store/slices/authStore.ts`
typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
// import { immer } from 'zustand/middleware/immer'; // If using immer

interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null; // Assuming UserProfile type from shared/types
  token: string | null;
  mfaRequired: boolean;
  loading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegistrationData) => Promise<void>;
  logout: () => Promise<void>;
  setToken: (token: string | null) => void;
  setUser: (user: UserProfile | null) => void;
  setMfaRequired: (required: boolean) => void;
  // ... other actions
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      user: null,
      token: null,
      mfaRequired: false,
      loading: false,
      error: null,
      login: async (credentials) => {
        set({ loading: true, error: null });
        try {
          // const response = await authService.login(credentials); // Call actual service
          // Simulate API call for now
          await new Promise(resolve => setTimeout(resolve, 1000));
          const mockUser: UserProfile = { id: '1', email: credentials.email, fullName: 'Test User', /* ... other fields */ };
          const mockToken = 'mock-jwt-token';

          set({ isAuthenticated: true, user: mockUser, token: mockToken, loading: false, mfaRequired: false /* or true based on API response */ });
          localStorage.setItem('authToken', mockToken); // Or handle token in persist middleware
        } catch (err: any) {
          set({ error: err.message || 'Login failed', loading: false, isAuthenticated: false });
          throw err;
        }
      },
      register: async (data) => { /* ... similar logic ... */ },
      logout: async () => {
        // await authService.logout(); // Call actual service
        set({ isAuthenticated: false, user: null, token: null, mfaRequired: false });
        localStorage.removeItem('authToken');
      },
      setToken: (token) => set({ token, isAuthenticated: !!token }),
      setUser: (user) => set({ user }),
      setMfaRequired: (required) => set({ mfaRequired: required }),
      // ...
    }),
    {
      name: 'auth-storage', // name of the item in the storage (must be unique)
      storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
      partialize: (state) => ({ token: state.token, user: state.user, isAuthenticated: state.isAuthenticated }), // Persist only token, user, isAuthenticated
    }
  )
);

*   Other stores (`userProfileStore`, `projectStore`, `creativeEditorStore`, `templateStore`, `subscriptionStore`, `developerPortalStore`) will follow a similar pattern, managing their respective states and actions, and interacting with corresponding services.

### 5.5 API Services (`src/services/`)
#### 5.5.1 `apiClient.ts`
*   **Purpose:** Centralized Axios instance for API calls.
*   **Logic:**
    typescript
    import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from 'axios';
    import { useAuthStore } from '@/app/store/slices/authStore'; // For accessing token and logout action

    const apiClient: AxiosInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // From .env
      headers: {
        'Content-Type': 'application/json',
      },
    });

    apiClient.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = useAuthStore.getState().token; // Get token from Zustand store
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    apiClient.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access, e.g., logout user
          useAuthStore.getState().logout();
          // Optionally redirect to login page
          // window.location.href = '/login';
        }
        // Handle other global errors if needed
        return Promise.reject(error);
      }
    );

    export default apiClient;
    
*   **Requirement Mapping:** NFR-001.

#### 5.5.2 Feature-Specific Services
Each feature module (e.g., `src/features/auth/services/authService.ts`) will have its own service file that uses the `apiClient` to make specific API calls.
Example: `src/features/auth/services/authService.ts`
typescript
import apiClient from '@/services/apiClient';
import { LoginCredentials, UserProfile, RegistrationData } from '@/shared/types/api'; // Assuming types are defined

const login = async (credentials: LoginCredentials): Promise<{ token: string, user: UserProfile }> => {
  const response = await apiClient.post('/auth/login', credentials); // Endpoint from apiEndpoints.ts
  return response.data;
};

const register = async (data: RegistrationData): Promise<UserProfile> => {
  const response = await apiClient.post('/auth/register', data);
  return response.data;
};
// ... other auth related API calls (verifyEmail, requestPasswordReset, etc.)

export const authService = {
  login,
  register,
  // ...
};


### 5.6 Internationalization (`src/app/i18n/`, `src/locales/`)
#### 5.6.1 `src/app/i18n/index.ts`
*   **Purpose:** Configure i18next.
*   **Logic:**
    typescript
    import i18n from 'i18next';
    import { initReactI18next } from 'react-i18next';
    import LanguageDetector from 'i18next-browser-languagedetector';
    import HttpApi from 'i18next-http-backend'; // For loading translations from /public/locales

    i18n
      .use(HttpApi) // Loads translations from /public/locales/{lng}/translation.json
      .use(LanguageDetector) // Detects user language
      .use(initReactI18next) // Passes i18n instance to react-i18next
      .init({
        supportedLngs: ['en-US', 'en-GB', 'es-ES', 'es-MX', 'fr-FR', 'de-DE'], // From requirements
        fallbackLng: 'en-US',
        debug: import.meta.env.DEV, // Enable debug output in development
        detection: {
          order: ['localStorage', 'navigator', 'htmlTag'],
          caches: ['localStorage'],
        },
        backend: {
          loadPath: '/locales/{{lng}}/{{ns}}.json', // Path to translation files
        },
        interpolation: {
          escapeValue: false, // React already safes from xss
        },
        // ns: ['translation'], // Default namespace
        // defaultNS: 'translation',
      });

    export default i18n;
    
*   **Requirement Mapping:** UI-006, PLI-001 to PLI-007.

#### 5.6.2 `src/locales/en/translation.json` (Example)
*   **Purpose:** Store English translation strings.
*   **Logic:** JSON key-value pairs.
    json
    {
      "welcomeMessage": "Welcome to CreativeFlow AI!",
      "loginPage": {
        "title": "Login",
        "emailLabel": "Email Address",
        "passwordLabel": "Password"
      },
      "dashboard": {
          "title": "Dashboard",
          "recentProjects": "Recent Projects"
      }
      // ... more translations
    }
    
*   Similar files for other supported languages (`es/translation.json`, `fr/translation.json`, `de/translation.json`). Regional variations (`en-GB`, `es-MX`) will be handled by i18next fallback mechanisms or specific resource files if significant differences exist.

### 5.7 Theming (`src/app/theme/`)
#### 5.7.1 `index.ts` (or `theme.ts`)
*   **Purpose:** Define global theme variables.
*   **Logic:**
    typescript
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
      };
      typography: {
        fontFamily: string;
        fontSizeBase: string;
        h1Size: string;
        // ... other font sizes and weights
      };
      spacing: {
        xs: string;
        sm: string;
        md: string;
        lg: string;
        xl: string;
      };
      breakpoints: {
        sm: string; // e.g., '640px'
        md: string; // e.g., '768px'
        lg: string; // e.g., '1024px'
        xl: string; // e.g., '1280px'
      };
      // ... other theme properties like borderRadius, shadows
    }

    export const defaultTheme: AppTheme = {
      colors: {
        primary: '#6A1B9A', // Example: Purple
        secondary: '#4A148C',
        accent: '#F50057',
        background: '#F3E5F5',
        surface: '#FFFFFF',
        textPrimary: '#212121',
        textSecondary: '#757575',
        error: '#D32F2F',
        success: '#388E3C',
      },
      typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
        fontSizeBase: '16px',
        h1Size: '2.5rem',
        // ...
      },
      spacing: {
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px',
      },
      breakpoints: {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
      },
    };
    

#### 5.7.2 `ThemeProvider.tsx` (Optional, if using React Context for theme)
*   **Purpose:** Provides the theme to components via React Context.
*   **Logic:** Creates a React Context for the theme and provides `defaultTheme`. Could also support theme switching (light/dark).
    typescript
    // Example ThemeProvider.tsx
    import React, { createContext, useContext, useState, useMemo } from 'react';
    import { defaultTheme, AppTheme } from './theme'; // Assuming theme.ts is in the same folder

    interface ThemeContextType {
      theme: AppTheme;
      // toggleTheme?: () => void; // If theme switching is supported
    }

    const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

    export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
      // Basic theme provider, can be extended for theme switching
      const [currentTheme] = useState<AppTheme>(defaultTheme);

      const themeValue = useMemo(() => ({ theme: currentTheme }), [currentTheme]);

      return (
        <ThemeContext.Provider value={themeValue}>
          {children}
        </ThemeContext.Provider>
      );
    };

    export const useTheme = (): ThemeContextType => {
      const context = useContext(ThemeContext);
      if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
      }
      return context;
    };
    
    Alternatively, CSS custom properties can be set at the root level based on `defaultTheme`, and components use these variables.

### 5.8 Feature Modules
Each feature module will typically contain `pages/`, `components/`, `services/`, `hooks/`, and `types/` subdirectories as needed.

#### 5.8.1 Authentication (REQ-001, UAPM-1-001, UAPM-1-002, UAPM-1-006)
*   **Pages:**
    *   `src/features/auth/pages/LoginPage.tsx`: (REQ-001, UAPM-1-001) Renders `LoginForm` and `SocialLoginButtons`.
    *   `src/features/auth/pages/RegisterPage.tsx`: (REQ-001, UAPM-1-001) Renders `RegistrationForm` and `SocialLoginButtons`.
    *   `src/features/auth/pages/EmailVerificationPage.tsx`: (REQ-001, UAPM-1-001) Handles email verification link/code submission.
    *   `src/features/auth/pages/ForgotPasswordPage.tsx`: (UAPM-1-006) Form to request password reset.
    *   `src/features/auth/pages/ResetPasswordPage.tsx`: (UAPM-1-006) Form to set new password using reset token.
    *   `src/features/auth/pages/MfaSetupPage.tsx`: (UAPM-1-002) Guides user through MFA setup (TOTP QR code, SMS/Email verification).
    *   `src/features/auth/pages/MfaVerifyPage.tsx`: (UAPM-1-002) For users to enter MFA code during login.
*   **Components:**
    *   `src/features/auth/components/LoginForm.tsx`: (REQ-001, UAPM-1-001) Inputs for email, password.
    *   `src/features/auth/components/RegistrationForm.tsx`: (REQ-001, UAPM-1-001) Inputs for email, password, full name (optional). Handles GDPR consent checkbox.
    *   `src/features/auth/components/SocialLoginButton.tsx`: Reusable button for Google, Facebook, Apple login.
    *   `src/features/auth/components/MfaRecoveryCodesDisplay.tsx`: Shows recovery codes to user.
*   **Services:** `src/features/auth/services/authService.ts`: Functions for `login()`, `register()`, `verifyEmail()`, `initiateSocialLogin()`, `completeSocialLogin()`, `setupMfa()`, `verifyMfa()`, `requestPasswordReset()`, `resetPassword()`.
*   **State Integration:** Uses `useAuthStore`.

#### 5.8.2 Dashboard (UI-001, REQ-010, REQ-015)
*   **Pages:** `src/features/dashboard/pages/DashboardPage.tsx`.
*   **Components:**
    *   `RecentItemsCard.tsx`: (REQ-4-009) Displays recent projects, workbenches, templates.
    *   `QuickActions.tsx`: (UI-001) Buttons for "New Creative", "Browse Templates".
    *   `UsageStatsWidget.tsx`: (REQ-015, UAPM-1-005) Displays credits remaining, generations this month, subscription plan.
    *   `ProgressIndicatorsWidget.tsx`: (UI-001) Shows ongoing AI generations.
    *   `PersonalizedTipsWidget.tsx`: (UI-001) Displays recommendations.
*   **Services:** `src/features/dashboard/services/dashboardService.ts`: Fetches data for dashboard widgets.
*   **State Integration:** May use `userProfileStore`, `projectStore`, `templateStore`.

#### 5.8.3 Creative Editor (UI-002, REQ-005, REQ-006, REQ-008, REQ-011, REQ-012, REQ-013)
*   **Pages:** `src/features/creativeEditor/pages/CreativeEditorPage.tsx`.
*   **Components:**
    *   `Canvas.tsx`: (UI-002) Main WYSIWYG editing area. Renders elements, handles selection, drag-and-drop.
        *   Incorporates platform-specific safe zone indicators (REQ-012, SMPIO-010).
        *   Displays collaborator cursors/selections (REQ-013, REQ-WCI-008).
    *   `Toolbar.tsx`: (UI-002) Tools for text, shapes, image upload, AI generation trigger, zoom, undo/redo.
    *   `PropertiesPanel.tsx`: (UI-002) Contextual panel to edit properties of selected element.
    *   `AssetPicker.tsx`: (REQ-011, REQ-4-004) Allows picking assets from user library or stock assets.
    *   `SamplePreviewGrid.tsx`: (REQ-008) Displays 4 low-res AI generation samples. Allows selection and regeneration.
    *   `AiSuggestionsPanel.tsx`: (REQ-006) Displays AI-powered suggestions for layouts, colors, elements.
    *   `PlatformPreviewToggle.tsx`: (REQ-012, SMPIO-013) Allows toggling platform-specific preview contexts.
    *   `EditorErrorFeedback.tsx`: (REQ-WCI-008, REQ-007.1) Displays errors related to editor actions or AI generation.
*   **Services:** `src/features/creativeEditor/services/editorService.ts` (local editor actions), `aiGenerationService.ts` (interacts with backend for AI features).
*   **State Integration:** Heavy use of `creativeEditorStore`.
*   **CRDT Integration:** Utilities/hooks in `src/features/creativeEditor/collab/` to integrate with Yjs (or equivalent) and the `CollaborationService` via WebSockets. Handles merging of local and remote changes. (REQ-013, REQ-5-002).

#### 5.8.4 Template Gallery (UI-003, REQ-005, REQ-022)
*   **Pages:** `src/features/templateGallery/pages/TemplateGalleryPage.tsx`.
*   **Components:**
    *   `TemplateCard.tsx`: Displays a single template preview and information.
    *   `TemplateFilters.tsx`: (UI-003) Filters by category, platform, industry, style.
    *   `TemplateSearchBar.tsx`: (UI-003) Keyword search for templates.
    *   `TrendingTemplatesSection.tsx`, `NewTemplatesSection.tsx`, `RecommendedTemplatesSection.tsx`: (REQ-WCI-010).
    *   `UserTemplateSaveModal.tsx`: (REQ-WCI-010) For Pro+ users to save designs as private templates.
    *   `InspirationGallerySection.tsx`: (REQ-WCI-010, REQ-9-008) Showcases UGC.
*   **Services:** `src/features/templateGallery/services/templateService.ts`: Fetches templates, categories, saves user templates.
*   **State Integration:** `templateStore`.

#### 5.8.5 User Profile & Account Management (REQ-004, UAPM-1-003 to UAPM-1-005, UAPM-1-007, UAPM-1-009, UAPM-1-010, REQ-6-005)
*   **Pages:** `src/features/profile/pages/ProfilePage.tsx` (tabbed interface for sub-sections).
    *   Sub-sections/routes: `/profile/info`, `/profile/security` (password, MFA), `/profile/brand-kits`, `/profile/subscription`, `/profile/privacy`, `/profile/notifications-settings`.
*   **Components:**
    *   `ProfileInfoForm.tsx`: (UAPM-1-003) Edit full name, username, profile picture, language, timezone.
    *   `PasswordChangeForm.tsx`: (UAPM-1-006).
    *   `MfaSettings.tsx`: (UAPM-1-002) Enable/disable MFA methods, view recovery codes.
    *   `BrandKitList.tsx`, `BrandKitEditor.tsx`: (UAPM-1-004).
    *   `SubscriptionDetailsDisplay.tsx`: (UAPM-1-005, REQ-6-005) View current tier, billing history link, manage subscription link.
    *   `DataPrivacyControls.tsx`: (UAPM-1-007) Request data access, portability, deletion.
    *   `ConsentManagement.tsx`: (UAPM-1-009) View and withdraw consents.
    *   `ActiveSessionsManager.tsx`: (UAPM-1-008) View and revoke active sessions.
    *   `TeamRoleDisplay.tsx`: (UAPM-1-010).
*   **Services:** `src/features/profile/services/userProfileService.ts`, `brandKitService.ts`, `billingService.ts` (facade to backend).
*   **State Integration:** `userProfileStore`, `authStore`, `subscriptionStore`.

#### 5.8.6 Workbench & Project Management (REQ-010, REQ-011, REQ-4-001 to REQ-4-009)
*   **Pages:**
    *   `src/features/workbench/pages/WorkbenchListPage.tsx`.
    *   `src/features/workbench/pages/WorkbenchDetailPage.tsx` (might show projects list).
    *   `src/features/project/pages/ProjectListPage.tsx` (can be part of WorkbenchDetail or standalone).
    *   `src/features/project/pages/ProjectDetailPage.tsx` (shows assets, history, links to editor).
*   **Components:**
    *   `WorkbenchCard.tsx`, `ProjectCard.tsx`.
    *   `CreateWorkbenchModal.tsx`, `CreateProjectModal.tsx`.
    *   `AssetLibraryView.tsx`: (REQ-4-004) Upload, view, manage input assets.
    *   `GeneratedAssetHistory.tsx`: (REQ-4-005) List AI-generated assets with metadata.
    *   `AssetVersionHistoryViewer.tsx`: (REQ-4-006) Show versions of an asset.
    *   `ExportAssetModal.tsx`: (REQ-4-007) Select export format, resolution.
    *   `PlatformOptimizationSettings.tsx`: (REQ-4-008) Select target platform for optimizations.
*   **Services:** `src/features/workbench/services/workbenchService.ts`, `src/features/project/services/projectService.ts`, `src/features/asset/services/assetService.ts`.
*   **State Integration:** `projectStore`.

#### 5.8.7 Collaboration Features (Client-side UI for REQ-013, REQ-5-001, REQ-WCI-008, REQ-14-010)
*   This is primarily integrated into the Creative Editor feature.
*   **WebSocket Integration:** `src/services/collaborationSocket.ts` (or similar) to connect to `REPO-COLLABORATION-SERVICE-001`.
    *   Manages WebSocket connection.
    *   Sends local CRDT updates.
    *   Receives remote CRDT updates and applies them to local Yjs doc.
    *   Handles presence events (join, leave, cursor movements).
*   **UI Components (within Editor):**
    *   `CollaboratorAvatars.tsx`: Displays avatars of active collaborators.
    *   `RemoteCursor.tsx`: Renders cursors of other users on the canvas.
    *   `ElementLockIndicator.tsx`: Shows if an element is being edited by another user.
*   **Hooks:** `useCollaboration(projectId)`: Hook to manage Yjs document, provider, and collaboration state.
*   **State Integration:** `creativeEditorStore` for `isCollaborating`, `collaborators` list.

#### 5.8.8 API Developer Portal (Client-Side for REQ-017, REQ-018, REQ-7-005)
*   **Pages:** `src/features/developer/pages/DeveloperPortalPage.tsx` (tabbed interface).
    *   Sub-sections: `/developer/api-keys`, `/developer/webhooks`, `/developer/documentation` (link or embed).
*   **Components:**
    *   `ApiKeyManager.tsx`: List, create, revoke API keys. Display key once on creation.
    *   `WebhookManager.tsx`: List, create, update, delete webhook endpoints. Test webhook.
    *   `ApiUsageDisplay.tsx`: Shows API usage and quota status.
*   **Services:** `src/features/developer/services/developerApiService.ts`.
*   **State Integration:** `developerPortalStore`.

### 5.9 Shared Components (`src/shared/components/`)
Organized by Atomic Design principles (atoms, molecules, organisms) or by common UI patterns.
#### 5.9.1 Atoms
*   `Button.tsx`: (REQ-WCI-003) Various styles (primary, secondary, text, icon), sizes, disabled state. Accessible.
*   `Input.tsx`: Text, password, email, number inputs with labels, validation messages, icons.
*   `Icon.tsx`: Wrapper for SVG icons.
*   `Typography.tsx`: Components for h1-h6, p, span, applying theme typography.
*   `Spinner.tsx`: Loading indicator.
*   `Checkbox.tsx`, `Radio.tsx`, `Switch.tsx`.
#### 5.9.2 Molecules
*   `Modal.tsx`: Reusable modal dialog.
*   `Card.tsx`: Generic card component for dashboard items, templates.
*   `NotificationToast.tsx`: For displaying success/error/info messages.
*   `Dropdown.tsx`: Select component.
*   `Tooltip.tsx`: (REQ-WCI-003) Contextual help.
*   `SearchBar.tsx`.
*   `FileUpload.tsx`: Component for handling file uploads.
#### 5.9.3 Organisms
*   `Header.tsx`: Main application header with navigation, user menu, notifications.
*   `Sidebar.tsx`: Main navigation sidebar (if applicable to layout).
*   `Footer.tsx`.
*   `DataTable.tsx`: Reusable table component for displaying lists of items (e.g., projects, assets, API keys).
*   `ConfirmationDialog.tsx`: Generic dialog for confirming actions (e.g., delete).
#### 5.9.4 Layouts
*   `src/shared/components/layouts/PublicLayout.tsx`: Layout for unauthenticated pages (e.g., Login, Register).
*   `src/shared/components/layouts/AppLayout.tsx`: Main layout for authenticated users, typically includes Header, Sidebar/Main content area.

### 5.10 Shared Hooks (`src/shared/hooks/`)
*   `useAuth.ts`: (As described in file structure) Interacts with `useAuthStore`.
*   `useApi.ts`: Generic hook for making API calls, handling loading/error states.
    typescript
    // Example useApi.ts
    import { useState, useCallback } from 'react';
    import apiClient from '@/services/apiClient';
    import { AxiosRequestConfig, AxiosError } from 'axios';

    interface UseApiOptions<T> {
      initialData?: T | null;
    }

    interface UseApiReturn<T, P = any> {
      data: T | null;
      loading: boolean;
      error: AxiosError | null;
      request: (params?: P, config?: AxiosRequestConfig) => Promise<T | null>;
    }

    function useApi<T = any, P = any>(
      apiCall: (params?: P, config?: AxiosRequestConfig) => Promise<T>,
      options?: UseApiOptions<T>
    ): UseApiReturn<T, P> {
      const [data, setData] = useState<T | null>(options?.initialData || null);
      const [loading, setLoading] = useState<boolean>(false);
      const [error, setError] = useState<AxiosError | null>(null);

      const request = useCallback(
        async (params?: P, config?: AxiosRequestConfig): Promise<T | null> => {
          setLoading(true);
          setError(null);
          try {
            const result = await apiCall(params, config);
            setData(result);
            setLoading(false);
            return result;
          } catch (err: any) {
            setError(err);
            setLoading(false);
            // Consider global error notification here
            return null;
          }
        },
        [apiCall]
      );
      return { data, loading, error, request };
    }
    export default useApi;
    
*   `usePwaUpdate.ts`: (If using `vite-plugin-pwa` or similar, it might provide its own hook like `useRegisterSW`). Manages PWA update detection and prompt.
*   `useDebounce.ts`: For debouncing input (e.g., search fields).
*   `useLocalStorage.ts`: Hook for easily managing state in local storage.
*   `useTheme.ts`: (As defined in ThemeProvider example).
*   `useMediaQuery.ts`: Hook for responsive design logic based on breakpoints.

### 5.11 Utilities (`src/shared/utils/`)
*   `dateUtils.ts`: Format dates, times, relative time (using a library like `date-fns` or `dayjs`).
*   `validationUtils.ts`: Common input validation functions (e.g., email format, password strength).
*   `localStorageUtils.ts`: Typed wrappers for localStorage get/set.
*   `tokenUtils.ts`: Functions for decoding JWT (`jwt-decode`), checking expiration.
*   `pwaUtils.ts`: Helper functions related to PWA features (e.g., checking for standalone mode).

### 5.12 Types (`src/shared/types/`)
*   `api.d.ts`: API DTOs (as described above).
*   `domain.d.ts`: Client-side specific domain models. Example:
    typescript
    // src/shared/types/domain.d.ts
    export interface User { // Client-side representation, may differ from API UserProfile
      id: string;
      email: string;
      fullName?: string;
      // ...
    }

    export interface EditorElement {
      id: string;
      type: 'text' | 'image' | 'shape';
      x: number;
      y: number;
      width: number;
      height: number;
      content?: string; // For text
      src?: string; // For image
      // ... other properties
    }

    export interface UINotification {
        id: string;
        message: string;
        type: 'success' | 'error' | 'info' | 'warning';
        duration?: number;
    }
    

## 6. Error Handling and Logging

### 6.1 Client-Side Error Handling
*   **API Errors:** `apiClient.ts` response interceptor will handle common HTTP errors (401, 403, 500).
    *   401: Logout user, redirect to login.
    *   403: Display "Access Denied" message.
    *   500/Other: Display generic error message, log details.
*   **Component Errors:** Use React Error Boundaries for critical sections of the UI to prevent the entire app from crashing. Log errors caught by boundaries.
*   **Form Validation Errors:** Display inline messages next to form fields.
*   **User Feedback:** Use `NotificationToast.tsx` for user-friendly error messages (REQ-WCI-008).
*   **Requirement Mapping:** REQ-007.1 (AI Gen errors), REQ-WCI-008.

### 6.2 Logging Strategy
*   **Development:** Log extensively to the browser console (debug, info, warn, error).
*   **Production:**
    *   Log critical errors and unhandled exceptions.
    *   Consider integrating a client-side error tracking service (e.g., Sentry, Rollbar - though not explicitly in tech stack, can be added if QA-003 implies client-side error tracking setup). For now, console logging for errors that can be reported by users.
    *   `reportWebVitals` can send performance data to an analytics endpoint or a logging service.

## 7. Performance Considerations (NFR-001)

*   **Code Splitting & Lazy Loading:** Use `React.lazy` and `Suspense` for route-based code splitting and lazy loading of large components/modules to improve initial load time (LCP REQ-SSPE-022).
*   **Memoization:** Use `React.memo`, `useMemo`, and `useCallback` judiciously to prevent unnecessary re-renders of components.
*   **Optimizing API Calls:**
    *   Fetch only necessary data.
    *   Debounce frequent calls (e.g., search suggestions).
    *   Use caching strategies (client-side or service worker) for GET requests.
*   **PWA Caching:** Leverage service worker caching for app shell and static assets (REQ-WCI-001).
*   **Image Optimization:** Use optimized image formats (e.g., WebP where supported), lazy load images below the fold.
*   **Bundle Size Analysis:** Regularly analyze production bundle size using tools like `vite-plugin-visualizer` or `source-map-explorer` to identify and optimize large chunks.
*   **Requirement Mapping:** REQ-WCI-002 (UI responsiveness), REQ-SSPE-001, REQ-SSPE-003, REQ-SSPE-004, REQ-SSPE-022.

## 8. Security Considerations

*   **JWT Handling:**
    *   Store JWTs securely (e.g., `localStorage` is common, but consider `HttpOnly` cookies if a BFF architecture is used and can set them; for SPA with direct API Gateway calls, `localStorage` with XSS mitigation is typical).
    *   Handle token expiration and implement refresh token logic if provided by backend. `jwt-decode` can be used to check expiry.
    *   Clear tokens on logout.
*   **Input Validation:** Perform client-side validation for user inputs to provide immediate feedback, but always rely on backend validation as the source of truth.
*   **XSS Prevention:** React inherently escapes content rendered in JSX, which helps prevent XSS. Avoid using `dangerouslySetInnerHTML` unless absolutely necessary and with sanitized content.
*   **Secure API Communication:** All API calls must use HTTPS.
*   **CSRF Protection:** If using cookie-based sessions (less likely with JWTs in `localStorage`), ensure backend provides CSRF protection mechanisms (e.g., anti-CSRF tokens). For JWTs in headers, CSRF is generally less of a concern for the API calls themselves.
*   **Dependency Vulnerabilities:** Regularly scan dependencies for known vulnerabilities (e.g., using `npm audit` or Snyk, as part of CI/CD - REQ-20-005).

## 9. Testing Strategy
(This section outlines the setup and types of tests within this repository. QA-001, QA-002 cover broader strategy)
*   **Unit Testing:**
    *   **Tools:** Jest, React Testing Library.
    *   **Scope:** Individual components (rendering, props, event handling), utility functions, hooks, Zustand store actions/reducers.
    *   **Coverage:** Aim for >=90% for critical logic and UI components (as per REQ-QAS-001).
*   **Integration Testing:**
    *   **Tools:** React Testing Library (for component integration), Jest (for service/store integration).
    *   **Scope:** Interactions between multiple components, components with state stores, components with services (mocking API calls).
*   **E2E Testing (Setup/Stubs):**
    *   **Tools:** Configuration for Cypress or Playwright.
    *   **Scope:** Critical user journeys (Login, Registration, Create Basic Creative). Actual test scripts might reside in a separate E2E testing repository or be developed progressively. This repo will contain necessary `data-testid` attributes and configurations to support E2E testing.
    *   **Requirement Mapping:** REQ-QAS-003.
*   **Accessibility Testing:**
    *   **Tools:** `@axe-core/react` for automated checks during development/CI, manual testing with screen readers.
    *   **Scope:** Adherence to WCAG 2.1 AA.
*   **PWA Testing:** Manually test installability, offline functionality, update prompts on various browsers/devices.
*   **Test Execution:** Automated tests (unit, integration) run on every commit/PR via CI/CD pipeline (PMDT-003).

## 10. Build and Deployment

### 10.1 Vite Configuration Highlights (`vite.config.ts`)
*   React plugin (`@vitejs/plugin-react`).
*   PWA plugin (`vite-plugin-pwa`) for service worker generation and manifest injection.
*   Environment variable handling (e.g., `VITE_` prefix).
*   Build optimizations (minification, code splitting, tree shaking - default with Vite).
*   Proxy setup for development (if API gateway is on a different port/domain).
*   Output directory configuration.
*   Base path configuration if deployed to a subfolder.

### 10.2 Environment Variables (`.env.example`, `.env`)
*   `VITE_API_BASE_URL`: Base URL for the backend API Gateway.
*   `VITE_NOTIFICATION_SERVICE_WS_URL`: WebSocket URL for Notification Service.
*   `VITE_COLLABORATION_SERVICE_WS_URL`: WebSocket URL for Collaboration Service.
*   `VITE_GA_MEASUREMENT_ID` (if Google Analytics is used client-side).
*   `VITE_MIXPANEL_TOKEN` / `VITE_AMPLITUDE_API_KEY` (if used client-side).
*   `VITE_SENTRY_DSN` (if Sentry used client-side).

## 11. Third-Party Libraries Justification
*   **`axios`:** Mature, widely-used HTTP client for making API requests. Supports interceptors, cancellation, and easy error handling.
*   **`zustand`:** Simple, flexible, and performant state management library for React. Less boilerplate than Redux, good for both global and local/feature state.
*   **`react-router-dom`:** Standard library for client-side routing in React applications.
*   **`i18next` (with `react-i18next`):** Powerful and flexible internationalization framework. Supports multiple backends for translation loading, pluralization, context, etc.
*   **`jwt-decode`:** Small utility to decode JWT tokens on the client-side to inspect payload (e.g., user roles, expiry) without needing crypto libraries.
*   **`workbox` (via `vite-plugin-pwa`):** Simplifies service worker development, providing robust caching strategies and lifecycle management.
*   **(Potentially) `date-fns` or `dayjs`:** For client-side date/time formatting and manipulation, offering better tree-shakability and immutability than Moment.js.
*   **(Potentially) A UI Component Library (e.g., Material UI, Ant Design, Chakra UI):** If rapid UI development with pre-built, accessible components is prioritized over custom styling. (Not explicitly stated, so assuming custom components with a theming solution for now).
*   **(Potentially) Drag-and-Drop library (e.g., `react-beautiful-dnd`, `dnd-kit`):** For implementing drag-and-drop in the creative editor and asset management.

## 12. Future Considerations / Scalability
*   **Micro-Frontend Decomposition:** If the application grows significantly, specific features (e.g., Creative Editor, Admin Panel) could be further decoupled into true micro-frontends using techniques like module federation.
*   **Performance Optimization:** Continuous monitoring (RUM) and profiling to identify bottlenecks. Advanced techniques like virtualized lists for large data sets.
*   **Enhanced Offline Capabilities:** For more complex offline editing in the PWA, IndexedDB usage might be expanded, requiring more sophisticated data synchronization and conflict resolution logic on the client.
*   **WebAssembly (WASM):** For performance-critical client-side tasks (e.g., complex image processing in the editor, if not offloaded to backend AI).
*   **Real-time Collaboration Enhancements:** Advanced CRDT features or optimizations for very large documents or high numbers of collaborators.
*   **State Management Evolution:** If state becomes extremely complex, migration to Redux Toolkit with its ecosystem (RTK Query, Redux Saga) could be considered, though Zustand is designed to scale well.

This SDS provides a detailed blueprint for the CreativeFlow.WebApp.PWA, aligning with user requirements, architectural decisions, and technology choices.