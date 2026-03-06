/**
 * DataForge Health Check
 *
 * Monitors the DataForge data intelligence engine health endpoints.
 * Critical priority - core service for data operations.
 */

import { ApiCheck, AssertionBuilder, RetryStrategyBuilder } from 'checkly/constructs'

// Main health endpoint check
new ApiCheck('dataforge-health-main', {
  name: 'DataForge - Main Health',
  degradedResponseTime: 1000,
  maxResponseTime: 2000,

  request: {
    method: 'GET',
    url: '{{DATAFORGE_BASE_URL}}/health',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      AssertionBuilder.jsonBody('$.service').equals('dataforge'),
      AssertionBuilder.responseTime().lessThan(2000),
    ],
  },

  runParallel: true,
  activated: true,
  muted: false,
  shouldFail: false,

  retryStrategy: RetryStrategyBuilder.fixedStrategy({
    baseBackoffSeconds: 0,
    maxRetries: 1,
    maxDurationSeconds: 600,
    sameRegion: false,
  }),

  locations: ['us-east-1', 'us-west-1'],
  frequency: 5, // Every 5 minutes

  tags: ['env:prod', 'service:dataforge', 'type:health', 'priority:critical'],
})

// Database health endpoint check
new ApiCheck('dataforge-health-db', {
  name: 'DataForge - Database Health',
  degradedResponseTime: 500,
  maxResponseTime: 1500,

  request: {
    method: 'GET',
    url: '{{DATAFORGE_BASE_URL}}/health/db',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      AssertionBuilder.jsonBody('$.checks.database.status').equals('healthy'),
      AssertionBuilder.responseTime().lessThan(1500),
      // Ensure database latency is reasonable
      AssertionBuilder.jsonBody('$.checks.database.latency_ms').lessThan(100),
    ],
  },

  runParallel: true,
  activated: true,
  muted: false,
  shouldFail: false,

  retryStrategy: RetryStrategyBuilder.fixedStrategy({
    baseBackoffSeconds: 0,
    maxRetries: 1,
    maxDurationSeconds: 600,
    sameRegion: false,
  }),

  locations: ['us-east-1', 'us-west-1'],
  frequency: 5,

  tags: ['env:prod', 'service:dataforge', 'type:health', 'priority:critical', 'component:database'],
})
