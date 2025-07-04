import { chromium, type FullConfig } from '@playwright/test';
import { AUTH_FILE } from '../playwright.config';
import 'dotenv/config';

/**
 * This function runs once before all tests. It logs in a default test user
 * and saves the authentication state (cookies, local storage) to a file.
 * This file is then used by all subsequent test suites to start in an
 * authenticated state, dramatically speeding up test execution by bypassing
 * the UI login for most specs.
 * @param config The full Playwright configuration object.
 */
async function globalSetup(config: FullConfig) {
  const { baseURL } = config.projects[0].use;
  const userEmail = process.env.STAGING_USER_EMAIL;
  const userPassword = process.env.STAGING_USER_PASSWORD;

  if (!baseURL || !userEmail || !userPassword) {
    throw new Error('baseURL, STAGING_USER_EMAIL, or STAGING_USER_PASSWORD environment variables are not set.');
  }

  // Launch a browser instance.
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to the login page.
    await page.goto(baseURL);
    await page.getByLabel('Email').fill(userEmail);
    await page.getByLabel('Password').fill(userPassword);
    await page.getByRole('button', { name: 'Login' }).click();

    // Wait for the dashboard to load to confirm successful login.
    // This is a critical step to ensure we are properly authenticated.
    await page.waitForURL('**/dashboard');
    await page.getByRole('button', { name: 'New Creative' }).waitFor({ state: 'visible', timeout: 10000 });

    // Save the authentication state to the specified file.
    await page.context().storageState({ path: AUTH_FILE });
    console.log(`Authentication state saved to ${AUTH_FILE}`);
  } catch (error) {
    console.error('Global setup failed:', error);
    throw error;
  } finally {
    // Close the browser.
    await browser.close();
  }
}

export default globalSetup;