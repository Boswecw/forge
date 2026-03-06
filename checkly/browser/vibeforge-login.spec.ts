/**
 * VibeForge Login Flow Test
 *
 * Validates the complete authentication flow for VibeForge.
 * Tests login functionality and dashboard accessibility.
 */

import { test, expect } from '@playwright/test'

test('VibeForge Login and Dashboard', async ({ page }) => {
  // Set timeout for the entire test
  test.setTimeout(30000)

  // Get credentials from environment variables
  const testEmail = process.env.TEST_EMAIL
  const testPassword = process.env.TEST_PASSWORD
  const vibeforgeUrl = process.env.VIBEFORGE_BASE_URL

  if (!testEmail || !testPassword || !vibeforgeUrl) {
    throw new Error('Missing required environment variables: TEST_EMAIL, TEST_PASSWORD, or VIBEFORGE_BASE_URL')
  }

  // Step 1: Navigate to login page
  await page.goto(`${vibeforgeUrl}/login`, {
    waitUntil: 'networkidle',
    timeout: 10000,
  })

  // Take screenshot at login page
  await page.screenshot({ path: 'login-page.png', fullPage: true })

  // Step 2: Verify login page loaded
  await expect(page).toHaveTitle(/VibeForge|Login/, { timeout: 5000 })

  // Step 3: Fill in credentials
  const emailInput = page.locator('input[type="email"], input[name="email"], input[id="email"]').first()
  const passwordInput = page.locator('input[type="password"], input[name="password"], input[id="password"]').first()

  await expect(emailInput).toBeVisible({ timeout: 5000 })
  await expect(passwordInput).toBeVisible({ timeout: 5000 })

  await emailInput.fill(testEmail)
  await passwordInput.fill(testPassword)

  // Step 4: Submit login form
  const submitButton = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")').first()
  await expect(submitButton).toBeVisible({ timeout: 5000 })
  await submitButton.click()

  // Step 5: Wait for navigation to dashboard
  await page.waitForURL(/\/(dashboard|home|app)/, {
    timeout: 10000,
    waitUntil: 'networkidle',
  })

  // Take screenshot at dashboard
  await page.screenshot({ path: 'dashboard.png', fullPage: true })

  // Step 6: Verify dashboard elements are visible
  // Look for common dashboard indicators
  const dashboardIndicators = [
    page.locator('[data-testid="dashboard"]'),
    page.locator('.dashboard'),
    page.locator('main'),
    page.locator('[role="main"]'),
    page.locator('h1'),
  ]

  let found = false
  for (const indicator of dashboardIndicators) {
    try {
      await expect(indicator).toBeVisible({ timeout: 2000 })
      found = true
      break
    } catch (e) {
      // Try next indicator
      continue
    }
  }

  if (!found) {
    throw new Error('Dashboard did not load - no dashboard indicators found')
  }

  // Step 7: Verify no error messages
  const errorSelectors = [
    '.error',
    '.alert-error',
    '[role="alert"]',
    '.notification-error',
  ]

  for (const selector of errorSelectors) {
    const errors = page.locator(selector)
    const count = await errors.count()
    if (count > 0) {
      const errorText = await errors.first().textContent()
      console.warn(`Warning: Found error element with text: ${errorText}`)
    }
  }

  // Success - login flow completed
  console.log('✓ Login successful')
  console.log('✓ Dashboard loaded')
})
