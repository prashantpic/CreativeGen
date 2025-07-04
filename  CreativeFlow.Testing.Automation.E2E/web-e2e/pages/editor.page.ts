import { type Page, type Locator } from '@playwright/test';

/**
 * Represents the Creative Editor page where users generate and manipulate creatives.
 * Encapsulates locators and actions available within the editor.
 */
export class EditorPage {
  readonly page: Page;
  readonly promptInput: Locator;
  readonly generateSamplesButton: Locator;
  readonly samplePreviewContainer: Locator;
  readonly generateHighResButton: Locator;
  readonly canvas: Locator;

  constructor(page: Page) {
    this.page = page;
    this.promptInput = page.getByPlaceholder('Describe your creative idea...');
    this.generateSamplesButton = page.getByRole('button', { name: 'Generate Samples' });
    this.samplePreviewContainer = page.locator('[data-testid="sample-preview-container"]');
    this.generateHighResButton = page.getByRole('button', { name: 'Generate High-Resolution' });
    this.canvas = page.locator('[data-testid="editor-canvas"]');
  }

  /**
   * Enters the given text into the AI prompt input field.
   * @param text The prompt text for AI generation.
   */
  async enterPrompt(text: string): Promise<void> {
    await this.promptInput.fill(text);
  }

  /**
   * Clicks the button to start the sample generation process.
   */
  async clickGenerateSamples(): Promise<void> {
    await this.generateSamplesButton.click();
  }

  /**
   * Selects a generated sample by its index.
   * @param index The zero-based index of the sample to select.
   */
  async selectSample(index: number): Promise<void> {
    await this.samplePreviewContainer.locator('[data-testid="sample-item"]').nth(index).click();
  }

  /**
   * Returns the main canvas locator for further assertions or interactions.
   * @returns The Locator for the editor canvas.
   */
  async getCanvas(): Promise<Locator> {
    return this.canvas;
  }
}