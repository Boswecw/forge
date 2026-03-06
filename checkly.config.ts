import { defineConfig } from 'checkly'
import { Frequency } from 'checkly/constructs'

/**
 * Checkly Configuration for Forge Ecosystem
 * 
 * Environment Variables Required (set in Checkly Dashboard):
 * - RAKE_BASE_URL
 * - DATAFORGE_BASE_URL
 * - NEUROFORGE_BASE_URL
 * - VIBEFORGE_BASE_URL
 * - TEST_EMAIL
 * - TEST_PASSWORD
 */

export default defineConfig({
  projectName: 'Forge Ecosystem Monitoring',
  logicalId: 'forge-monitoring',
  
  repoUrl: 'https://github.com/your-org/forge-monorepo', // UPDATE THIS
  
  checks: {
    // Global defaults for all checks
    activated: true,
    muted: false,
    runtimeId: '2024.02', // Checkly runtime version

    // Default frequency (can be overridden per check)
    frequency: Frequency.EVERY_5M,

    // Locations to run checks from
    locations: ['us-east-1', 'us-west-1', 'eu-west-1'],

    // Tags applied to all checks (can be extended per check)
    tags: ['forge-ecosystem'],

    // Environment variables (loaded from process.env for local testing)
    environmentVariables: [
      {
        key: 'RAKE_BASE_URL',
        value: process.env.RAKE_BASE_URL || 'https://rake-production.onrender.com',
      },
      {
        key: 'DATAFORGE_BASE_URL',
        value: process.env.DATAFORGE_BASE_URL || 'https://dataforge.onrender.com',
      },
      {
        key: 'NEUROFORGE_BASE_URL',
        value: process.env.NEUROFORGE_BASE_URL || 'https://neuroforge.onrender.com',
      },
      {
        key: 'VIBEFORGE_BASE_URL',
        value: process.env.VIBEFORGE_BASE_URL || 'https://vibeforge.com',
      },
      {
        key: 'TEST_EMAIL',
        value: process.env.TEST_EMAIL || 'test@example.com',
      },
      {
        key: 'TEST_PASSWORD',
        value: process.env.TEST_PASSWORD || 'change-me',
      },
    ],
    
    // Glob pattern for check files (API checks, etc.)
    checkMatch: ['**/__checks__/**/*.check.ts', '**/api/**/*.check.ts'],

    // Browser check defaults
    browserChecks: {
      frequency: Frequency.EVERY_10M,
      testMatch: '**/browser/**/*.spec.ts',
    },
  },
  
  cli: {
    // Run directory for checks
    runLocation: 'us-east-1',
    
    // Files to include when deploying
    reporters: ['list'],
  },
})
