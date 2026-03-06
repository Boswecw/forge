# Checkly Setup Guide

Complete step-by-step guide to get Forge Ecosystem monitoring up and running.

## Prerequisites

- Node.js 18+ installed
- Checkly account (free tier available)
- GitHub repository set up
- Services deployed and accessible

## Step 1: Create Checkly Account

1. Go to [https://www.checklyhq.com/](https://www.checklyhq.com/)
2. Sign up for a free account
3. Verify your email

## Step 2: Get API Credentials

1. Log into Checkly dashboard
2. Go to **Settings → Account Settings**
3. Navigate to **API Keys** tab
4. Click **Create API Key**
5. Name it "Forge Ecosystem CI/CD"
6. Copy the **API Key** and **Account ID**

Save these securely - you'll need them for GitHub Actions.

## Step 3: Configure Environment Variables in Checkly

1. In Checkly dashboard, go to **Settings → Environment Variables**
2. Add the following variables:

```
RAKE_BASE_URL=https://rake.boswelldigital.com
DATAFORGE_BASE_URL=https://dataforge.boswelldigital.com
NEUROFORGE_BASE_URL=https://neuroforge.boswelldigital.com
VIBEFORGE_BASE_URL=https://vibeforge.com
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-secure-test-password
```

3. Click **Save**

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret** and add:

```
CHECKLY_API_KEY=cu_xxx (from Step 2)
CHECKLY_ACCOUNT_ID=xxx (from Step 2)
RAKE_BASE_URL=https://rake.boswelldigital.com
DATAFORGE_BASE_URL=https://dataforge.boswelldigital.com
NEUROFORGE_BASE_URL=https://neuroforge.boswelldigital.com
VIBEFORGE_BASE_URL=https://vibeforge.com
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-secure-test-password
```

## Step 5: Test Locally (Optional but Recommended)

```bash
# Navigate to ecosystem directory
cd /home/charlie/Forge/ecosystem

# Set environment variables locally
export CHECKLY_API_KEY=your-api-key
export CHECKLY_ACCOUNT_ID=your-account-id
export RAKE_BASE_URL=https://rake.boswelldigital.com
export DATAFORGE_BASE_URL=https://dataforge.boswelldigital.com
export NEUROFORGE_BASE_URL=https://neuroforge.boswelldigital.com
export VIBEFORGE_BASE_URL=https://vibeforge.com
export TEST_EMAIL=test@example.com
export TEST_PASSWORD=your-password

# Test all checks
npm run checkly:test

# Test specific check
npx checkly test --check rake-health-main
```

If tests pass locally, proceed to deployment!

## Step 6: Initial Deployment

```bash
# Deploy all checks to Checkly
npm run checkly:deploy
```

This will:
- Create all checks in your Checkly account
- Set up the monitoring schedule
- Make checks visible in the dashboard

## Step 7: Verify Deployment

1. Go to Checkly dashboard
2. Navigate to **Checks**
3. You should see:
   - `rake-health-main`
   - `rake-health-redis`
   - `dataforge-health-main`
   - `dataforge-health-db`
   - `neuroforge-health-main`
   - `neuroforge-health-models`
   - `vibeforge-login-flow`

4. Click on any check to view:
   - Check configuration
   - Run history
   - Response times
   - Results from different locations

## Step 8: Configure Alerts (Optional)

### Slack Integration

1. Create a Slack webhook:
   - Go to [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
   - Click **Create New App**
   - Choose **From Scratch**
   - Name: "Checkly Forge Monitoring"
   - Select your workspace
   - Go to **Incoming Webhooks**
   - Activate webhooks
   - Click **Add New Webhook to Workspace**
   - Select channel (e.g., #forge-monitoring)
   - Copy the webhook URL

2. Add to Checkly:
   - Go to **Settings → Alert Channels**
   - Click **Add Alert Channel**
   - Select **Slack**
   - Paste webhook URL
   - Name it "Forge Slack Alerts"
   - **Save**

3. Uncomment the alert channel code in `checkly/alerts/slack-channel.ts`

4. Redeploy:
   ```bash
   npm run checkly:deploy
   ```

### Email Alerts

1. In Checkly dashboard, go to **Settings → Alert Channels**
2. Click **Add Alert Channel**
3. Select **Email**
4. Enter email address: `alerts@boswelldigital.com`
5. Configure:
   - ✅ Send on failure
   - ✅ Send on recovery
   - ❌ Send on degraded (optional)
6. **Save**

### Webhook for ForgeCommand (Future)

When ForgeCommand webhook endpoint is ready:

1. Update `FORGE_COMMAND_WEBHOOK_URL` in environment variables
2. Uncomment webhook code in `checkly/alerts/slack-channel.ts`
3. Redeploy checks

## Step 9: Enable GitHub Actions

The workflow is already configured in `.github/workflows/checkly.yml`.

To activate it:

1. **Push to Main**:
   ```bash
   git add .
   git commit -m "feat: add Checkly monitoring infrastructure"
   git push origin main
   ```

2. **Verify Workflow**:
   - Go to GitHub repository
   - Click **Actions** tab
   - You should see "Checkly Monitoring" workflow
   - First run will deploy checks

3. **Future Deployments**:
   - Any changes to `checkly/**` on main branch will auto-deploy
   - Pull requests will run tests before merge

## Step 10: Monitor Your Monitors

### Checkly Dashboard

- **Checks** - View all checks and their status
- **Monitoring** - Real-time uptime and performance graphs
- **Alerting** - Review alert history
- **Analytics** - Long-term trends and insights

### What to Watch For

1. **False Positives** - Adjust thresholds if too sensitive
2. **Degraded Performance** - Indicates service slowdown
3. **Regional Failures** - Network or region-specific issues
4. **Alert Noise** - Too many alerts? Increase frequency or adjust thresholds

## Troubleshooting

### "Check not found" Error

```bash
# List all checks
npx checkly list

# Force create check
npm run checkly:deploy -- --force
```

### Environment Variables Not Working

1. Verify variables are set in Checkly dashboard
2. Check spelling and casing (must match exactly)
3. Try using `process.env.VARIABLE_NAME` in checks

### Playwright Browser Issues

```bash
# Install browsers with dependencies
npx playwright install --with-deps chromium

# Test browser locally
npx playwright test
```

### GitHub Actions Failing

1. Verify secrets are set correctly
2. Check workflow logs for specific errors
3. Test locally first: `npm run checkly:test`

## Maintenance

### Weekly Tasks

- Review check results in dashboard
- Verify no persistent failures
- Check response time trends

### Monthly Tasks

- Review and optimize check frequencies
- Update test credentials if needed
- Verify alert channels are working
- Check Checkly usage/costs

### As Needed

- Add new checks for new services
- Update environment URLs when deploying changes
- Adjust thresholds based on real performance

## Cost Management

### Free Tier Limits

- 10,000 check runs/month
- 5,000 browser check minutes/month

### Current Usage Estimate

- ~43,400 runs/month with current setup
- Requires **paid plan** ($7/month for 100,000 runs)

### Optimization Tips

1. **Reduce Frequency** - Critical: 5min → 10min saves 50%
2. **Fewer Locations** - 2 locations → 1 location saves 50%
3. **Combine Checks** - Merge similar checks where possible
4. **Disable Non-Critical** - Pause checks for dev/staging environments

## Next Steps

1. ✅ Complete setup (Steps 1-10)
2. Monitor for 1 week - verify checks are reliable
3. Configure additional alert channels as needed
4. Add more checks for additional services (AuthorForge, WebSafe)
5. Integrate with ForgeCommand dashboard

## Resources

- [Checkly Documentation](https://www.checklyhq.com/docs/)
- [Checkly API Reference](https://www.checklyhq.com/docs/api/)
- [Playwright Docs](https://playwright.dev/)
- [Forge Ecosystem Docs](../docs/README.md)

## Support

For help:
- **Checkly Issues** - [Checkly Support](https://www.checklyhq.com/support)
- **Setup Issues** - Check this guide or README.md
- **Forge Services** - Contact Boswell Digital Solutions

---

**Setup Complete!** 🎉

Your Forge Ecosystem is now monitored 24/7 with Checkly.
