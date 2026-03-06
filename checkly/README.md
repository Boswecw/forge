# Forge Ecosystem Checkly Monitoring

## Documentation Contract

- **Repo type:** Workspace monitoring surface
- **Authority boundary:** External monitoring configuration for Forge services; not a resident Forge runtime and not the durable truth store
- **Deep reference:** `../docs/canonical/documentation_protocol_v1.md`
- **README role:** Monitoring overview and operator entrypoint
- **Truth note:** Check lists, monitored endpoints, and operational coverage in this README are snapshot facts unless explicitly marked as canonical doctrine

Comprehensive monitoring infrastructure for all Forge services using Checkly's checks-as-code approach.

## Overview

This monitoring setup provides:

- **API Health Checks** - Monitor service health endpoints every 5-10 minutes
- **Browser Checks** - Validate authentication flows and critical user paths
- **Multi-Region Monitoring** - Check from US East, US West, and EU West
- **Alerting** - Slack, webhook, and email notifications on failures
- **CI/CD Integration** - Automated testing and deployment via GitHub Actions

## Services Monitored

| Service | Health Endpoint | Check Frequency | Priority |
|---------|----------------|-----------------|----------|
| **Rake** | `/health`, `/health/redis` | 5 min | Critical |
| **DataForge** | `/health`, `/health/db` | 5 min | Critical |
| **NeuroForge** | `/health`, `/health/full` | 10 min | Standard |
| **VibeForge** | Browser login flow | 10 min | Standard |

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Set these in the Checkly dashboard (Settings → Environment Variables):

```bash
# Service URLs
RAKE_BASE_URL=https://rake.boswelldigital.com
DATAFORGE_BASE_URL=https://dataforge.boswelldigital.com
NEUROFORGE_BASE_URL=https://neuroforge.boswelldigital.com
VIBEFORGE_BASE_URL=https://vibeforge.com

# Test Credentials
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-test-password

# Alert Configuration (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
FORGE_COMMAND_WEBHOOK_URL=https://your-webhook-url
ALERT_EMAIL=alerts@boswelldigital.com
```

### 3. Test Checks Locally

```bash
# Test all checks
npm run checkly:test

# Test specific check
npx checkly test --check rake-health-main
```

### 4. Deploy to Checkly

```bash
# Deploy all checks
npm run checkly:deploy

# Deploy and force update
npx checkly deploy --force
```

## Check Structure

```
checkly/
├── api/                          # API health checks
│   ├── rake-health.check.ts     # Rake service monitoring
│   ├── dataforge-health.check.ts # DataForge monitoring
│   └── neuroforge-health.check.ts # NeuroForge monitoring
├── browser/                      # Browser checks
│   └── vibeforge-login.check.ts # VibeForge login flow
├── alerts/                       # Alert configurations
│   └── slack-channel.ts         # Slack integration setup
└── __checks__/                   # Shared utilities
    └── utils.ts                 # Common helpers
```

## Check Configuration

### API Checks

Each API check includes:

- **Status Code Validation** - Assert 200 OK
- **Response Time Thresholds** - Degraded (1-1.5s), Max (2-3s)
- **JSON Body Assertions** - Validate health status and components
- **Double Check** - Verify failure from second location before alerting
- **Multi-Region** - Run from multiple AWS regions

Example:

```typescript
new ApiCheck('service-health', {
  name: 'Service - Health Check',
  request: {
    method: 'GET',
    url: '{{SERVICE_URL}}/health',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.status').equals('healthy'),
      AssertionBuilder.responseTime().lessThan(2000),
    ],
  },
  frequency: 5,
  doubleCheck: true,
  tags: ['env:prod', 'service:name', 'type:health', 'priority:critical'],
})
```

### Browser Checks

Browser checks use Playwright to:

- Navigate through authentication flows
- Verify page loads and element visibility
- Take screenshots on failure
- Validate no error messages appear

Example:

```typescript
new BrowserCheck('login-flow', {
  name: 'Service - Login Flow',
  frequency: Frequency.EVERY_10M,
  code: {
    content: test('Login', async ({ page }) => {
      await page.goto(process.env.SERVICE_URL!)
      await page.fill('input[type="email"]', process.env.TEST_EMAIL!)
      await page.fill('input[type="password"]', process.env.TEST_PASSWORD!)
      await page.click('button[type="submit"]')
      await page.waitForURL(/dashboard/)
      await expect(page.locator('.dashboard')).toBeVisible()
    }),
  },
  tags: ['env:prod', 'service:name', 'type:browser', 'priority:standard'],
})
```

## Alerting Strategy

### Trigger Conditions

- **2 Consecutive Failures** - Double-check before alerting
- **Degraded Performance** - Response time exceeds threshold
- **Recovery** - Service returns to healthy state

### Alert Channels

1. **Slack** - Primary notification channel
   - Sends to `#forge-monitoring`
   - Includes service name, status, response time, error message
   - Links to detailed results

2. **Webhook** - ForgeCommand integration
   - JSON payload with full check details
   - Enables dashboard notifications
   - Signed with Checkly signature

3. **Email** - Fallback for critical failures
   - Only for priority:critical checks
   - Sent to operations team

### Alert Message Template

```
*Service*: DataForge - Main Health
*Status*: 🔴 Failed
*Response Time*: 2456ms
*Location*: us-east-1
*Error*: Connection timeout after 2000ms

*Action Required*: Investigate immediately
```

## CI/CD Integration

### GitHub Actions Workflow

The `.github/workflows/checkly.yml` workflow:

1. **On Pull Request** - Test checks before merge
2. **On Push to Main** - Deploy checks to Checkly
3. **Daily Schedule** - Health check of monitoring itself

### Required GitHub Secrets

Set these in your repository settings (Settings → Secrets):

```bash
CHECKLY_API_KEY=cu_xxx
CHECKLY_ACCOUNT_ID=xxx
RAKE_BASE_URL=https://...
DATAFORGE_BASE_URL=https://...
NEUROFORGE_BASE_URL=https://...
VIBEFORGE_BASE_URL=https://...
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-password
```

### Workflow Triggers

```yaml
# Test on PR
on:
  pull_request:
    paths:
      - 'checkly/**'

# Deploy on merge
on:
  push:
    branches:
      - main
```

## Tags System

All checks use tags for filtering and organization:

- `env:prod` / `env:staging` - Environment
- `service:<name>` - Service identifier
- `type:health` / `type:browser` - Check type
- `priority:critical` / `priority:standard` - Alert urgency
- `component:<name>` - Specific component (database, redis, etc.)

### Filtering Examples

```bash
# All critical checks
--tags "priority:critical"

# All Rake checks
--tags "service:rake"

# All health checks
--tags "type:health"

# Combine filters
--tags "service:dataforge,type:health"
```

## Troubleshooting

### Check Failures

1. **Verify Service Health** - Check service is actually running
2. **Check Environment Variables** - Ensure URLs are correct
3. **Review Check Logs** - Look for specific error messages
4. **Test Locally** - Run `npm run checkly:test` with same env vars

### Common Issues

**Missing Environment Variables**
```bash
Error: Missing required environment variables: TEST_EMAIL, TEST_PASSWORD
```
→ Configure in Checkly dashboard: Settings → Environment Variables

**Playwright Browser Not Found**
```bash
npx playwright install --with-deps chromium
```

**Check Times Out**
- Increase `maxResponseTime` in check configuration
- Verify service isn't under heavy load
- Check network connectivity from Checkly regions

### Debug Mode

```bash
# Run with debug output
CHECKLY_DEBUG=1 npm run checkly:test

# Run specific check with verbose logging
npx checkly test --check vibeforge-login-flow --verbose
```

## Best Practices

### Writing Checks

1. **Use Shared Utilities** - Import from `__checks__/utils.ts`
2. **Handle Async Properly** - Always await promises
3. **Set Appropriate Timeouts** - Don't make them too tight
4. **Take Screenshots on Failure** - Helps debugging
5. **Test Locally First** - Before deploying

### Maintaining Checks

1. **Version Control** - Commit all check changes
2. **Review PRs** - CI tests checks before deployment
3. **Monitor Alert Noise** - Adjust thresholds if too many false positives
4. **Update Documentation** - Keep this README current

### Performance Tips

1. **Avoid Unnecessary Checks** - Don't duplicate coverage
2. **Use Appropriate Frequencies** - Critical: 5min, Standard: 10min
3. **Limit Locations** - More locations = more costs
4. **Set Realistic Timeouts** - Based on actual service performance

## Costs

Checkly pricing is based on:

- Number of check runs per month
- Number of locations
- Browser check minutes

**Estimated Monthly Runs:**
- 3 critical API checks × 2 locations × 5min frequency = ~26,000 runs
- 2 standard API checks × 1 location × 10min frequency = ~8,700 runs
- 1 browser check × 2 locations × 10min frequency = ~8,700 runs

**Total: ~43,400 runs/month**

Free tier: 10,000 runs/month
Paid plans start at $7/month for 100,000 runs

## Additional Resources

- [Checkly Documentation](https://www.checklyhq.com/docs/)
- [Playwright Documentation](https://playwright.dev/)
- [Forge Ecosystem Architecture](../docs/architecture/FORGE_UNIFIED_ARCHITECTURE.md)
- [Health Endpoint Contract](./checkly-context.md)

## Support

For issues with:
- **Monitoring Setup** - Check this README
- **Service Health** - Check service logs
- **Checkly Platform** - Contact Checkly support
- **Forge Ecosystem** - Contact Boswell Digital Solutions

---

**Last Updated:** December 17, 2025
**Maintained By:** Boswell Digital Solutions LLC
**Monitoring Status:** ✅ Active
