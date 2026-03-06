/**
 * Slack Alert Channel Configuration
 *
 * Configure this alert channel in the Checkly dashboard or via environment variables.
 * This file serves as documentation for the alert strategy.
 */

import { SlackAlertChannel } from 'checkly/constructs'

/**
 * Slack webhook alert channel
 *
 * Setup Instructions:
 * 1. Create a Slack webhook: https://api.slack.com/messaging/webhooks
 * 2. Set SLACK_WEBHOOK_URL in Checkly dashboard environment variables
 * 3. Uncomment the code below once webhook is configured
 */

// Uncomment when SLACK_WEBHOOK_URL is configured
/*
export const slackChannel = new SlackAlertChannel('forge-slack-alerts', {
  name: 'Forge Slack Notifications',

  // Webhook URL from environment variable
  url: process.env.SLACK_WEBHOOK_URL!,

  // Alert on 2 consecutive failures (double check)
  sendFailure: true,
  sendRecovery: true,
  sendDegraded: true,

  // Custom alert templates
  channel: '#forge-monitoring', // Update to your Slack channel

  // Alert message template
  template: {
    title: '{{CHECK_NAME}} {{#if IS_FAILURE}}Failed{{else if IS_DEGRADED}}Degraded{{else}}Recovered{{/if}}',

    text: `
*Service*: {{CHECK_NAME}}
*Status*: {{#if IS_FAILURE}}🔴 Failed{{else if IS_DEGRADED}}⚠️ Degraded{{else}}✅ Recovered{{/if}}
*Response Time*: {{RESPONSE_TIME}}ms
*Location*: {{RESULT_LOCATION}}
*Time*: {{CHECK_RESULT_CREATED_AT}}

{{#if ERROR_MESSAGE}}
*Error*: {{ERROR_MESSAGE}}
{{/if}}

{{#if IS_FAILURE}}
*Action Required*: Investigate immediately
{{/if}}

<{{CHECK_RESULT_URL}}|View Details>
    `.trim(),
  },
})
*/

/**
 * Webhook Alert Channel (for ForgeCommand integration)
 *
 * This will allow ForgeCommand to receive alerts and display them in the dashboard.
 * Webhook server runs on localhost:9999 when Forge-Command is running.
 */

import { WebhookAlertChannel } from 'checkly/constructs'

export const forgeCommandWebhook = new WebhookAlertChannel('forge-command-webhook', {
  name: 'ForgeCommand Webhook',

  url: process.env.FORGE_COMMAND_WEBHOOK_URL || 'http://localhost:9999/webhooks/checkly',

  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Checkly-Signature': '{{CHECKLY_SIGNATURE}}',
  },

  template: JSON.stringify({
    checkId: '{{CHECK_ID}}',
    checkName: '{{CHECK_NAME}}',
    checkType: '{{CHECK_TYPE}}',
    status: '{{CHECK_STATUS}}',
    isFailure: '{{IS_FAILURE}}',
    isDegraded: '{{IS_DEGRADED}}',
    responseTime: '{{RESPONSE_TIME}}',
    location: '{{RESULT_LOCATION}}',
    timestamp: '{{CHECK_RESULT_CREATED_AT}}',
    errorMessage: '{{ERROR_MESSAGE}}',
    resultUrl: '{{CHECK_RESULT_URL}}',
    tags: '{{CHECK_TAGS}}',
  }),

  sendFailure: true,
  sendRecovery: true,
  sendDegraded: true,
})

/**
 * Email Alert Channel
 *
 * Fallback alert method for critical failures.
 */

// Uncomment and configure when needed
/*
import { EmailAlertChannel } from 'checkly/constructs'

export const emailChannel = new EmailAlertChannel('forge-email-alerts', {
  name: 'Forge Email Notifications',

  address: process.env.ALERT_EMAIL || 'alerts@boswelldigital.com',

  sendFailure: true,
  sendRecovery: true,
  sendDegraded: false, // Only critical alerts via email
})
*/

// Export placeholder for type safety
export const alertChannels = {
  // Add configured alert channels here
}
