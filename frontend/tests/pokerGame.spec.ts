import { test, expect } from '@playwright/test';

test.describe('Poker Game End-to-End Test', () => {
  test('should allow players to start a game, bet, and fold', async ({ page }) => {

    await page.goto('/');

    
    const stackSizeInput = page.locator('input[name="stacksize"]');
    await stackSizeInput.fill('1000');
    
    await page.click('button:has-text("Apply")');
    
    const startButton = page.locator('button:has-text("Start")');
    await startButton.click();

   
    const gameLogs = page.locator('[data-testid="game-logs"]');
    await expect(gameLogs).toContainText('Player 1 is dealt');


    const betButton = page.locator('button:has-text("raise")');
    await betButton.click();

    await expect(gameLogs).toContainText('raises to');

    const foldButton = page.locator('button:has-text("fold")');
    await foldButton.click();

    await expect(gameLogs).toContainText('folds');
  });
});
