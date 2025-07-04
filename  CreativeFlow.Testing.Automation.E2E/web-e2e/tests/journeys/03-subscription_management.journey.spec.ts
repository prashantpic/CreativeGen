import { test, expect } from '@playwright/test';

// This describe block uses the authenticated state from global-setup
test.describe('Subscription Management Journey', () => {

  test('should allow a user to upgrade from Free to Pro', async ({ page }) => {
    // Setup: Ensure the test user is on a 'Free' plan. This should be done via API
    // in a `test.beforeEach` or by using a dedicated 'free plan' test user.
    
    // 1. Navigate to the account/billing page
    await page.goto('/account/billing');

    // 2. Click the "Upgrade to Pro" button
    const upgradeButton = page.getByRole('button', { name: 'Upgrade to Pro' });
    await expect(upgradeButton).toBeVisible();

    // 3. Intercept the Stripe/payment gateway call and mock a successful response.
    // This prevents the test from making a real payment.
    await page.route('**/api/v1/billing/stripe-checkout', async route => {
      console.log(`Intercepted: ${route.request().url()}`);
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Upgrade successful.',
          newPlan: 'Pro'
        }),
      });
    });

    await upgradeButton.click();
    
    // Here we'd typically interact with a Stripe modal/page.
    // For this test, we assume clicking "Upgrade" directly triggers the API.
    // If there's a UI flow, those steps would go here.
    
    // 4. Assert that the UI updates to show the "Pro" plan is active.
    const planIndicator = page.locator('[data-testid="current-plan-badge"]');
    await expect(planIndicator).toHaveText('Pro', { timeout: 10000 });

    // 5. Navigate to a Pro-only feature (e.g., Brand Kits) and assert that it is now accessible.
    await page.goto('/brand-kits');
    const createBrandKitButton = page.getByRole('button', { name: 'Create Brand Kit' });
    await expect(createBrandKitButton).toBeVisible();
    await expect(page.locator('[data-testid="pro-feature-lock"]')).not.toBeVisible();
  });
});