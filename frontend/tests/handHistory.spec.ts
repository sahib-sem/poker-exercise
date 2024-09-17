import { test, expect } from '@playwright/test';

test.describe('Hand History Integration Test', () => {
  
  test.beforeEach(async ({ page }) => {
    
    await page.route('**/api/v1/hands?status=completed', async (route) => {
     
        const mockHandHistory = [
            {
              id: '1',
              stack_size: 1000,
              dealer_idx: 0,
              small_blind_idx: 1,
              big_blind_idx: 2,
              players: [
                { player_idx: 0, winnings: 100, hole_cards: 'AhKh' },
                { player_idx: 1, winnings: 0, hole_cards: '2c3c' },
              ],
              actions: [
                { action_type: 'bet', amount: 100 },
                { action_type: 'raise', raise_amount: 200 },
                {action_type: 'call'},
                { action_type: 'deal', card_string: 'AhKh' },
                { action_type: 'check' },
                { action_type: 'check' },
                { action_type: 'deal', card_string: 'Jc' },
                { action_type: 'check' },
                { action_type: 'check' },
                { action_type: 'deal', card_string: 'Qh' },
                { action_type: 'bet', amount: 60 },
                { action_type: 'call' },
              ]
            }
          ];
      await route.fulfill({
        status: 200,
        body: JSON.stringify(mockHandHistory),
      });
    });
  });

  test('should display hand history correctly after fetching', async ({ page }) => {
    
    await page.goto('/');

    
    const handHistory = page.locator('[hand-data-testid="hand-history"]');
    await expect(handHistory).toContainText('Hand #1');
    await expect(handHistory).toContainText('b100:r200:c AhKh x:x Jc x:x Qh b60:c');
    await expect(handHistory).toContainText('Player 1: AhKh');
    await expect(handHistory).toContainText('Player 2: 2c3c');
  });

  test('should handle empty hand history', async ({ page }) => {
    
    await page.route('**/api/v1/hands?status=completed', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([]),
      });
    });

    await page.goto('/');

    const handHistory = page.locator('[hand-data-testid="hand-history"]');
    await expect(handHistory).toContainText('');
  });
});
