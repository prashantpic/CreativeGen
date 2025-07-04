import { type Page, type Locator } from '@playwright/test';

/**
 * Represents the Login page of the application.
 * Encapsulates all locators and actions related to the login functionality.
 */
export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email', { exact: true });
    this.passwordInput = page.getByLabel('Password', { exact: true });
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.locator('[data-testid="login-error-message"]');
  }

  /**
   * Performs the login action using the provided credentials.
   * @param email The user's email address.
   * @param password The user's password.
   */
  async login(email: string, password?: string): Promise<void> {
    await this.emailInput.fill(email);
    if (password) {
      await this.passwordInput.fill(password);
    }
    await this.loginButton.click();
  }

  /**
   * Retrieves the text content of the login error message.
   * @returns A promise that resolves to the error message text.
   */
  async getErrorMessage(): Promise<string | null> {
    await this.errorMessage.waitFor({ state: 'visible' });
    return this.errorMessage.textContent();
  }
}