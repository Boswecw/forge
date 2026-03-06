/**
 * Rake Health Check
 *
 * Monitors the Rake automated data ingestion pipeline health endpoints.
 * Critical priority - alerts immediately on failure.
 */

import { ApiCheck, AssertionBuilder, RetryStrategyBuilder } from 'checkly/constructs'

// Main health endpoint check
new ApiCheck('rake-health-main', {
  name: 'Rake - Main Health',
  degradedResponseTime: 1000,
  maxResponseTime: 2000,

  request: {
    method: 'GET',
    url: '{{RAKE_BASE_URL}}/health',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
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

  tags: ['env:prod', 'service:rake', 'type:health', 'priority:critical'],

  alertChannels: [], // Will be configured in Checkly dashboard
})

// Redis health endpoint check
new ApiCheck('rake-health-redis', {
  name: 'Rake - Redis Health',
  degradedResponseTime: 500,
  maxResponseTime: 1000,

  request: {
    method: 'GET',
    url: '{{RAKE_BASE_URL}}/health/redis',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      AssertionBuilder.jsonBody('$.checks.redis.status').equals('healthy'),
      AssertionBuilder.responseTime().lessThan(1000),
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

  tags: ['env:prod', 'service:rake', 'type:health', 'priority:critical', 'component:redis'],
})
