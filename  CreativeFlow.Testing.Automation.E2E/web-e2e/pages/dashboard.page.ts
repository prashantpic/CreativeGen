import { type Page, type Locator } from '@playwright/test';

/**
 * Represents the main Dashboard page, which is the landing page after a successful login.
 * Encapsulates locators and actions available on the dashboard.
 */
export class DashboardPage {
  readonly page: Page;
  readonly newCreativeButton: Locator;
  readonly recentProjectsList: Locator;
  readonly userProfileButton: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.newCreativeButton = page.getByRole('button', { name: 'New Creative' });
    this.recentProjectsList = page.locator('[data-testid="recent-projects-list"]');
    this.userProfileButton = page.locator('[data-testid="user-profile-avatar"]');
    this.logoutButton = page.getByRole('menuitem', { name: 'Log Out' });
  }

  /**
   * Clicks the 'New Creative' button to start a new project.
   */
  async clickNewCreative(): Promise<void> {
    await this.newCreativeButton.click();
  }

  /**
   * Gets the number of recent projects displayed on the dashboard.
   * @returns A promise that resolves to the count of recent project items.
   */
  async getRecentProjectCount(): Promise<number> {
    return this.recentProjectsList.locator('[data-testid="project-item"]').count();
  }

  /**
   * Logs the user out of the application.
   */
  async logout(): Promise<void> {
    await this.userProfileButton.click();
    await this.logoutButton.click();
  }
}