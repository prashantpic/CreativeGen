import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';
import { v4 as uuidv4 } from 'uuid';

test.describe('Authentication Journey', () => {

  // This test runs without using the saved auth state
  test.use({ storageState: { cookies: [], origins: [] } });
  test('should allow a new user to register successfully', async ({ page }) => {
    // This is a placeholder test. Real implementation requires navigating to register page.
    await page.goto('/register');
    const uniqueEmail = `testuser_${uuidv4()}@creativeflow.test`;
    await page.getByLabel('Full Name').fill('Test User');
    await page.getByLabel('Email').fill(uniqueEmail);
    await page.getByLabel('Password').fill('aSecurePassword123!');
    await page.getByRole('button', { name: 'Sign Up' }).click();

    await expect(page.locator('h1')).toHaveText('Please verify your email');
    // In a real scenario, this would involve using a mail-scraping service
    // to get the verification link and complete the flow.
  });

  // This test will use the default authenticated state from `global-setup.ts`
  test('should allow a verified user to log in', async ({ page }) => {
    // Since global-setup logs us in, we just need to verify we land on the dashboard.
    // The test starts on the base URL, which should redirect to the dashboard if authenticated.
    await page.goto('/');
    await expect(page).toHaveURL(/.*dashboard/);

    const dashboardPage = new DashboardPage(page);
    await expect(dashboardPage.newCreativeButton).toBeVisible();
  });

  // This test must start un-authenticated, so we override the storageState.
  test('should show an error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await page.goto('/');
    
    await loginPage.login('wronguser@example.com', 'wrongpassword');
    
    const errorMessage = await loginPage.getErrorMessage();
    await expect(errorMessage).toContain('Invalid email or password.');
    await expect(page).not.toHaveURL(/.*dashboard/);
  });
  
  // This test starts authenticated and then logs out.
  test('should allow a user to log out', async ({ page }) => {
    const dashboardPage = new DashboardPage(page);
    await page.goto('/dashboard');

    await dashboardPage.logout();

    // After logout, we should be redirected to the login page
    await expect(page).toHaveURL(/.*login/);
    const loginPage = new LoginPage(page);
    await expect(loginPage.loginButton).toBeVisible();
  });

});