import { test, expect } from '@playwright/test';
import { DashboardPage } from '../pages/dashboard.page';
import { EditorPage } from '../pages/editor.page';

// This entire describe block uses the authenticated state from global-setup
// by default, as configured in playwright.config.ts.
test.describe('Creative Workflow Journey', () => {
  
  test('should allow a user to create a new creative from start to finish', async ({ page }) => {
    const dashboardPage = new DashboardPage(page);
    const editorPage = new EditorPage(page);

    // 1. Navigate to the dashboard (or start there by default after login)
    await page.goto('/dashboard');
    await expect(dashboardPage.newCreativeButton).toBeVisible();

    // 2. Click the "New Creative" button
    await dashboardPage.clickNewCreative();

    // 3. Enter a project name (assuming a modal or new page appears)
    await page.waitForURL(/.*editor/);
    await expect(page.locator('h1')).toContainText('Editor'); // or similar check

    // 4. On the editor page, enter a text prompt into the prompt input field
    await editorPage.enterPrompt('A futuristic cityscape at sunset, synthwave style');

    // 5. Click the "Generate Samples" button
    await editorPage.clickGenerateSamples();

    // 6. Wait for the four sample previews to appear
    await expect(editorPage.samplePreviewContainer).toBeVisible({ timeout: 60000 }); // Long timeout for AI generation
    const sampleItems = editorPage.samplePreviewContainer.locator('[data-testid="sample-item"]');
    await expect(sampleItems).toHaveCount(4, { timeout: 30000 });

    // 7. Click on the first sample
    await editorPage.selectSample(0);
    // Add an assertion to check if the sample is highlighted or loaded into the main canvas
    await expect(sampleItems.nth(0)).toHaveClass(/selected/);

    // 8. Click a "Generate High-Resolution" button
    await editorPage.generateHighResButton.click();

    // 9. Wait for a success indicator or download button to become available
    const downloadButton = page.getByRole('button', { name: 'Download Asset' });
    await expect(downloadButton).toBeVisible({ timeout: 120000 }); // Longer timeout for final generation

    // 10. Assert that the final asset is available
    await expect(downloadButton).toBeEnabled();
  });
});