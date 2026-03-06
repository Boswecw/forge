/**
 * Shared Utilities for Checkly Checks
 *
 * Common assertions and helpers used across multiple checks.
 */

import { AssertionBuilder } from 'checkly/constructs'

/**
 * Standard health check assertions for Forge services
 */
export const standardHealthAssertions = [
  AssertionBuilder.statusCode().equals(200),
  AssertionBuilder.jsonBody('$.status').equals('healthy'),
  AssertionBuilder.jsonBody('$.service').isDefined(),
  AssertionBuilder.jsonBody('$.version').isDefined(),
  AssertionBuilder.jsonBody('$.timestamp').isDefined(),
]

/**
 * Database health check assertions
 */
export const databaseHealthAssertions = [
  ...standardHealthAssertions,
  AssertionBuilder.jsonBody('$.checks.database.status').equals('healthy'),
  AssertionBuilder.jsonBody('$.checks.database.latency_ms').lessThan(100),
]

/**
 * Redis health check assertions
 */
export const redisHealthAssertions = [
  ...standardHealthAssertions,
  AssertionBuilder.jsonBody('$.checks.redis.status').equals('healthy'),
  AssertionBuilder.jsonBody('$.checks.redis.latency_ms').lessThan(50),
]

/**
 * Common tags for production checks
 */
export const productionTags = ['env:prod', 'forge-ecosystem']

/**
 * Common locations for checks
 */
export const commonLocations = ['us-east-1', 'us-west-1']

/**
 * Standard retry strategy
 */
export const standardRetryStrategy = {
  type: 'fixed' as const,
  baseBackoffSeconds: 60,
  maxRetries: 2,
  maxDurationSeconds: 600,
  sameRegion: true,
}

/**
 * Critical service configuration (5 minute checks)
 */
export const criticalServiceConfig = {
  frequency: 5,
  doubleCheck: true,
  locations: commonLocations,
  degradedResponseTime: 1000,
  maxResponseTime: 2000,
}

/**
 * Standard service configuration (10 minute checks)
 */
export const standardServiceConfig = {
  frequency: 10,
  doubleCheck: true,
  locations: ['us-east-1'],
  degradedResponseTime: 1500,
  maxResponseTime: 3000,
}

/**
 * Helper function to create service-specific tags
 */
export function createServiceTags(
  service: string,
  type: 'health' | 'browser',
  priority: 'critical' | 'standard',
  component?: string
): string[] {
  const tags = [
    'env:prod',
    `service:${service}`,
    `type:${type}`,
    `priority:${priority}`,
  ]

  if (component) {
    tags.push(`component:${component}`)
  }

  return tags
}

/**
 * Helper to validate environment variables are present
 */
export function validateEnvVars(required: string[]): void {
  const missing = required.filter(key => !process.env[key])

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(', ')}\n` +
      'Please configure these in the Checkly dashboard or CI/CD secrets.'
    )
  }
}

/**
 * Common Playwright timeout configuration
 */
export const playwrightTimeouts = {
  test: 30000,
  navigation: 10000,
  action: 5000,
  assertion: 5000,
}

/**
 * Common error selectors for browser checks
 */
export const errorSelectors = [
  '.error',
  '.alert-error',
  '[role="alert"]',
  '.notification-error',
  '.toast-error',
  '[data-testid="error"]',
]

/**
 * Helper to take screenshot with timestamp
 */
export function getScreenshotPath(name: string): string {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  return `${name}-${timestamp}.png`
}
