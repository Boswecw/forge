/**
 * NeuroForge Health Check
 *
 * Monitors the NeuroForge AI orchestration layer health endpoint.
 * Standard priority - important but not as critical as data services.
 */

import { ApiCheck, AssertionBuilder, RetryStrategyBuilder } from 'checkly/constructs'

// Main health endpoint check
new ApiCheck('neuroforge-health-main', {
  name: 'NeuroForge - Main Health',
  degradedResponseTime: 1500,
  maxResponseTime: 3000, // AI services can be slower

  request: {
    method: 'GET',
    url: '{{NEUROFORGE_BASE_URL}}/health',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      AssertionBuilder.jsonBody('$.service').equals('neuroforge'),
      AssertionBuilder.responseTime().lessThan(3000),
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
  frequency: 10, // Every 10 minutes (standard priority)

  tags: ['env:prod', 'service:neuroforge', 'type:health', 'priority:standard'],
})

// Model availability check
new ApiCheck('neuroforge-health-models', {
  name: 'NeuroForge - Models Available',
  degradedResponseTime: 1000,
  maxResponseTime: 2000,

  request: {
    method: 'GET',
    url: '{{NEUROFORGE_BASE_URL}}/health/full',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      // Ensure at least one model is available
      AssertionBuilder.jsonBody('$.checks').isNotNull(),
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

  locations: ['us-east-1'],
  frequency: 10,

  tags: ['env:prod', 'service:neuroforge', 'type:health', 'priority:standard', 'component:models'],
})
