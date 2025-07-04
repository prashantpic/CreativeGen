# Software Design Specification (SDS) for CreativeFlow.Testing.Automation.E2E

## 1. Introduction

This document provides the detailed software design specification for the `CreativeFlow.Testing.Automation.E2E` repository. The primary purpose of this repository is to house, manage, and execute all automated End-to-End (E2E) and Performance tests for the CreativeFlow AI platform.

The specifications outlined herein are designed to be used for generating the test automation code. The chosen frameworks are:
*   **Web E2E Testing:** Playwright with TypeScript
*   **Mobile E2E Testing:** Flutter `integration_test` with Dart
*   **Performance Testing:** k6 with JavaScript/TypeScript

This document details the structure, test strategies, and specific implementation logic for each test suite and script.

### 1.1. Core Testing Principles
*   **Maintainability:** Tests will be structured using the Page Object Model (POM) for web tests and a similar finder/helper pattern for mobile to ensure easy updates when the UI changes.
*   **Reliability:** Tests will be designed to be resilient to minor UI fluctuations and will include robust waiting mechanisms and assertions. Flaky tests will be quarantined and fixed.
*   **Reusability:** Common user actions (e.g., login, creating a project) will be abstracted into reusable commands or helper functions.
*   **Clarity:** Test scripts will be written with clear, descriptive names for tests and steps, following a Behavior-Driven Development (BDD) style (`describe`, `it`, `expect`).
*   **CI/CD Integration:** All test suites are designed to be executed automatically within the CI/CD pipeline, providing rapid feedback on build quality.

## 2. Overall Test Architecture & Strategy

### 2.1. Web E2E Testing (Playwright)
The web E2E test suite will be structured to separate concerns:
*   **`playwright.config.ts`**: Central configuration for the test runner, defining projects for different browsers, base URLs, timeouts, and reporter settings.
*   **`tests/journeys/`**: Contains the test spec files, each focusing on a critical user journey. These files orchestrate the high-level flow of the test.
*   **`pages/`**: Implements the Page Object Model (POM). Each file in this directory represents a page or a major component of the application (e.g., `login.page.ts`, `dashboard.page.ts`). It will contain locators for UI elements and methods to interact with them.
*   **`support/`**: Contains global setup and reusable helper functions.
    *   `global-setup.ts`: Handles tasks that run once before all tests, such as logging in a default user and saving the authentication state to a file. This speeds up tests by bypassing the UI login for most specs.
    *   `helpers.ts`: Contains custom utility functions (e.g., generating random data).

### 2.2. Mobile E2E Testing (Flutter)
The mobile E2E tests will use Flutter's `integration_test` package, which runs tests directly on a device or emulator.
*   **`integration_test/journeys/`**: Contains the test files, each covering a critical mobile user journey.
*   **`integration_test/helpers/`**: Contains reusable helper functions and widget finders to avoid code duplication.
*   **`test_driver/`**: Contains the necessary driver script to execute the integration tests using `flutter drive`.

### 2.3. Performance Testing (k6)
k6 will be used for load, stress, and soak testing, primarily targeting the backend APIs.
*   **`scenarios/`**: Contains the k6 test scripts, each defining a specific performance test scenario (e.g., API load, AI generation throughput).
*   **`config/`**: Contains configuration files for different environments, defining base URLs, load profiles (VUs, duration), and thresholds.
*   **`lib/`**: Contains shared JavaScript/TypeScript modules for k6 scripts, such as authentication helpers or custom metrics reporting.

## 3. Detailed Component Specifications

### 3.1. General Configuration

#### 3.1.1. `package.json`
*   **Purpose:** To manage Node.js project dependencies and define test execution scripts.
*   **`dependencies` / `devDependencies`:**
    *   `@playwright/test`: Core Playwright test runner.
    *   `typescript`: For compiling TypeScript code.
    *   `@types/node`: Type definitions for Node.js.
    *   `k6`: k6 test runner (if using local execution via npm scripts).
    *   `@types/k6`: Type definitions for k6 scripts.
    *   `dotenv`: For managing environment variables.
*   **`scripts`:**
    *   `"test:e2e:web"`: `playwright test` - Runs all Playwright E2E tests.
    *   `"test:e2e:web:headed"`: `playwright test --headed` - Runs tests in a headed browser for debugging.
    *   `"test:e2e:web:report"`: `playwright show-report` - Opens the last test run report.
    *   `"test:perf:load:api"`: `k6 run performance/scenarios/api_load_test.js` - Executes the API load test.
    *   `"test:perf:load:ai"`: `k6 run performance/scenarios/ai_generation_load_test.js` - Executes the AI generation pipeline load test.
    *   `"test:perf:soak"`: `k6 run performance/scenarios/soak_test.js` - Executes the long-duration soak test.

#### 3.1.2. `tsconfig.json`
*   **Purpose:** To configure the TypeScript compiler for the Playwright and k6 test suites.
*   **`compilerOptions`:**
    *   `"target": "ES2022"`
    *   `"module": "commonjs"`
    *   `"strict": true`
    *   `"esModuleInterop": true`
    *   `"resolveJsonModule": true`
    *   `"outDir": "./dist"`
*   **`include`:**
    *   `["web-e2e/**/*.ts", "performance/**/*.ts", "performance/**/*.js"]`

### 3.2. Web E2E Tests (Playwright)

#### 3.2.1. `playwright.config.ts`
*   **Purpose:** Main configuration file for Playwright.
*   **Logic:**
    *   Define a `baseURL` pointing to the staging environment (e.g., `https://staging.creativeflow.ai`).
    *   Configure the `testDir` to point to `./web-e2e/tests`.
    *   Set up a `globalSetup` file (`./web-e2e/support/global-setup.ts`).
    *   Define `projects` to run tests across multiple browsers (Chromium, Firefox, WebKit).
    *   Configure `use` options:
        *   `headless: true` (for CI runs).
        *   `screenshot: 'only-on-failure'`.
        *   `video: 'retain-on-failure'`.
        *   `trace: 'on-first-retry'`.
    *   Configure reporters (e.g., `html`, `list`).

#### 3.2.2. `web-e2e/support/global-setup.ts`
*   **Purpose:** To perform a single login before all tests and save the state.
*   **Logic:**
    *   Defines an `async` function.
    *   Launches a browser instance using `chromium.launch()`.
    *   Creates a new page and navigates to the login page.
    *   Uses a pre-defined test user's credentials (from environment variables) to log in.
    *   Waits for the dashboard to load to confirm successful login.
    *   Saves the authentication state (cookies, local storage) to a file using `page.context().storageState({ path: 'auth.json' })`.
    *   Closes the browser.
    *   The `playwright.config.ts` will then use this `auth.json` file for subsequent tests, skipping the UI login step.

#### 3.2.3. `web-e2e/pages/` (Page Object Model files)
*   **`login.page.ts`**:
    *   **Properties**: `emailInput`, `passwordInput`, `loginButton`, `errorMessage`.
    *   **Methods**: `async login(email, password)`, `async getErrorMessage()`.
*   **`dashboard.page.ts`**:
    *   **Properties**: `newCreativeButton`, `recentProjectsList`.
    *   **Methods**: `async clickNewCreative()`, `async getRecentProjectCount()`.
*   **`editor.page.ts`**:
    *   **Properties**: `promptInput`, `generateSamplesButton`, `samplePreviewContainer`, `canvas`.
    *   **Methods**: `async enterPrompt(text)`, `async clickGenerateSamples()`, `async selectSample(index)`, `async getCanvas()`.

#### 3.2.4. `web-e2e/tests/journeys/01-auth.journey.spec.ts`
*   **Purpose:** To test the user authentication journey.
*   **Logic:**
    *   `test.describe('Authentication Journey')`:
        *   `test('should allow a new user to register successfully')`: Navigates to the registration page, fills in unique details, submits, and expects to be redirected to a "please verify email" page.
        *   `test('should allow a verified user to log in')`: This test will use the saved auth state from `global-setup.ts`. It will navigate directly to the dashboard and assert that the user is logged in.
        *   `test('should show an error for invalid credentials')`: Attempts to log in with incorrect credentials and asserts that an error message is visible.
        *   `test('should allow a user to log out')`: Navigates to the dashboard, finds the logout button, clicks it, and asserts that the user is redirected to the login page.

#### 3.2.5. `web-e2e/tests/journeys/02-creative_workflow.journey.spec.ts`
*   **Purpose:** To test the core creative generation workflow.
*   **Logic:**
    *   `test.describe('Creative Workflow Journey', () => { test.use({ storageState: 'auth.json' }); ... })`:
        *   `test('should allow a user to create a new creative from start to finish')`:
            1.  Navigate to the dashboard.
            2.  Click the "New Creative" button.
            3.  Enter a project name.
            4.  On the editor page, enter a text prompt into the prompt input field.
            5.  Click the "Generate Samples" button.
            6.  Wait for the four sample previews to appear (`expect(locator).toHaveCount(4)`).
            7.  Click on the first sample.
            8.  Click a "Generate High-Resolution" button.
            9.  Wait for a success indicator or download button to become available.
            10. Assert that the final asset is available.

#### 3.2.6. `web-e2e/tests/journeys/03-subscription_management.journey.spec.ts`
*   **Purpose:** To test subscription management flows.
*   **Logic:**
    *   `test.describe('Subscription Management Journey', () => { test.use({ storageState: 'auth.json' }); ... })`:
        *   `test('should allow a user to upgrade from Free to Pro')`:
            1.  (Setup: Ensure the test user is on a 'Free' plan).
            2.  Navigate to the account/billing page.
            3.  Click the "Upgrade to Pro" button.
            4.  Intercept the Stripe/payment gateway call and mock a successful response.
            5.  Assert that the UI updates to show the "Pro" plan is active.
            6.  Navigate to a Pro-only feature (e.g., Brand Kits) and assert that it is now accessible.

### 3.3. Mobile E2E Tests (Flutter `integration_test`)

#### 3.3.1. `mobile-e2e/pubspec.yaml`
*   **Purpose:** To manage mobile test dependencies.
*   **`dev_dependencies`:**
    *   `flutter_test`: `sdk: flutter`
    *   `integration_test`: `sdk: flutter`
    *   `flutter_driver`: `sdk: flutter`
    *   `test`: `^1.24.0`

#### 3.3.2. `mobile-e2e/integration_test/journeys/auth_journey_test.dart`
*   **Purpose:** To test the mobile authentication flow.
*   **Logic:**
    *   `void main() { integration_test.IntegrationTestWidgetsFlutterBinding.ensureInitialized(); ... }`
    *   `testWidgets('User can log in and log out successfully', (tester) async { ... })`:
        1.  Pump the main app widget: `await tester.pumpWidget(const MyApp());`.
        2.  Find the email and password `TextField` widgets using `find.byKey()` or `find.byType()`.
        3.  Enter text using `await tester.enterText()`.
        4.  Find and tap the login button: `await tester.tap(find.byKey(const Key('loginButton')));`.
        5.  Pump and settle to wait for animations and screen transitions: `await tester.pumpAndSettle();`.
        6.  Expect to find a widget unique to the dashboard screen (e.g., `find.byKey(const Key('dashboardWelcomeMessage'))`).
        7.  Find and tap the logout button.
        8.  Pump and settle.
        9.  Expect to find a widget unique to the login screen.

#### 3.3.3. `mobile-e2e/integration_test/journeys/offline_sync_journey_test.dart`
*   **Purpose:** To test offline editing and data synchronization.
*   **Logic:**
    *   `testWidgets('User can edit a project offline and sync changes upon reconnection', (tester) async { ... })`:
        1.  (Setup: Log in with an internet connection).
        2.  Navigate to a project and ensure it's loaded.
        3.  (Mock network disconnection: Use a mock HTTP client or a platform-specific method to simulate offline mode).
        4.  Find a text element on the canvas and tap it to edit.
        5.  Enter new text.
        6.  Assert that the local UI reflects the change.
        7.  (Mock network reconnection).
        8.  Trigger the sync process (e.g., by a button or automatically).
        9.  `await tester.pumpAndSettle();`.
        10. (Verification: Use an API helper to fetch the project state from the backend and assert that the changes are present).

### 3.4. Performance Tests (k6)

#### 3.4.1. `performance/config/environments.js`
*   **Purpose:** To provide environment-specific configurations.
*   **Logic:**
    javascript
    export const environments = {
      staging: {
        baseUrl: 'https://staging-api.creativeflow.ai',
        defaultUser: {
          email: process.env.STAGING_USER_EMAIL,
          password: process.env.STAGING_USER_PASSWORD,
        },
      },
      // ... other environments
    };
    

#### 3.4.2. `performance/scenarios/api_load_test.js`
*   **Purpose:** To load test core APIs.
*   **Logic:**
    *   `import http from 'k6/http';`
    *   `import { check, sleep, Trend } from 'k6';`
    *   `options`:
        *   `stages`: Define ramp-up to 10,000 VUs, sustain, and ramp-down.
        *   `thresholds`: Define P95 response time < 500ms for specific API tags or globally.
    *   `setup()`: A single VU logs in to get a JWT token to be used by all other VUs.
    *   `export default function (data)`:
        1.  Define request headers with the `Authorization: Bearer ${data.jwt}`.
        2.  Make `http.get` requests to core endpoints like `/api/v1/profile`, `/api/v1/projects`.
        3.  Use `check()` to assert `res.status === 200`.
        4.  Use `sleep()` to simulate user think time.

#### 3.4.3. `performance/scenarios/ai_generation_load_test.js`
*   **Purpose:** To test the throughput and latency of the AI generation pipeline.
*   **Logic:**
    *   `import http from 'k6/http';`
    *   `import { check, Trend } from 'k6';`
    *   `options`:
        *   `executor: 'constant-arrival-rate'`, `rate: 17`, `timeUnit: '1s'`, `duration: '10m'`.
        *   `thresholds`: Define P90 latency thresholds for sample and final generation steps.
    *   `setup()`: Get a JWT.
    *   `const sampleTrend = new Trend('sample_generation_latency');`
    *   `const finalTrend = new Trend('final_generation_latency');`
    *   `export default function (data)`:
        1.  Submit a generation request: `POST /api/v1/generations`.
        2.  Get the `generationId` from the response.
        3.  Poll the status endpoint `GET /api/v1/generations/${generationId}/status` in a loop until status is `AwaitingSelection` or `Completed`.
        4.  Record the total time for the sample generation phase in `sampleTrend`.
        5.  Submit a request to finalize the generation.
        6.  Poll again until `Completed`.
        7.  Record the total time for the final generation phase in `finalTrend`.

#### 3.4.4. `performance/scenarios/soak_test.js`
*   **Purpose:** To test system stability over a long period.
*   **Logic:**
    *   `import http from 'k6/http';`
    *   `options`:
        *   `executor: 'constant-vus'`, `vus: 500`, `duration: '4h'`.
    *   `export default function (data)`:
        *   Simulate a mix of user actions: GET profile, list projects, start a generation (without waiting for completion to avoid long-held VUs).
        *   The main goal is to keep a sustained load on the system. Validation occurs externally by monitoring Grafana dashboards for memory leaks, CPU creep, or increasing error rates over the 4-hour duration.