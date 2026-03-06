# Checkly Quick Start

Your Checkly account is configured! Here's how to get started.

## Your Credentials

```bash
Account ID: aa2e7e17-4d49-4c7f-99a4-ab852bafe8d6
API Key: cu_448b6c9d49e944f590cfcb98991f39a7
```

✅ Already saved in `.env.checkly` (not tracked in git)

## Quick Commands

### Test Locally (Recommended First Step)

```bash
# Option 1: Use the helper script
cd checkly
./test-local.sh

# Option 2: Manual with env vars
cd /home/charlie/Forge/ecosystem
export CHECKLY_API_KEY=cu_448b6c9d49e944f590cfcb98991f39a7
export CHECKLY_ACCOUNT_ID=aa2e7e17-4d49-4c7f-99a4-ab852bafe8d6
npm run checkly:test
```

### Deploy to Checkly

```bash
cd /home/charlie/Forge/ecosystem

# Load credentials
source .env.checkly

# Deploy all checks
npm run checkly:deploy
```

### View Your Checks

Dashboard: https://app.checklyhq.com/

## Before You Deploy

1. **Update Service URLs** in `.env.checkly`:
   ```bash
   RAKE_BASE_URL=https://your-actual-rake-url.com
   DATAFORGE_BASE_URL=https://your-actual-dataforge-url.com
   NEUROFORGE_BASE_URL=https://your-actual-neuroforge-url.com
   VIBEFORGE_BASE_URL=https://your-actual-vibeforge-url.com
   ```

2. **Add Test Credentials** in `.env.checkly`:
   ```bash
   TEST_EMAIL=your-test-account@example.com
   TEST_PASSWORD=your-test-password
   ```

3. **Test Locally First**:
   ```bash
   ./checkly/test-local.sh
   ```

4. **Deploy**:
   ```bash
   source .env.checkly && npm run checkly:deploy
   ```

## Next Steps

### 1. Configure Environment Variables in Checkly Dashboard

Go to [Settings → Environment Variables](https://app.checklyhq.com/settings/environment-variables)

Add these variables:
```
RAKE_BASE_URL=https://...
DATAFORGE_BASE_URL=https://...
NEUROFORGE_BASE_URL=https://...
VIBEFORGE_BASE_URL=https://...
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-password
```

### 2. Set Up GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions

Add these secrets:
```
CHECKLY_API_KEY=cu_448b6c9d49e944f590cfcb98991f39a7
CHECKLY_ACCOUNT_ID=aa2e7e17-4d49-4c7f-99a4-ab852bafe8d6
RAKE_BASE_URL=https://...
DATAFORGE_BASE_URL=https://...
NEUROFORGE_BASE_URL=https://...
VIBEFORGE_BASE_URL=https://...
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-password
```

### 3. Configure Slack Alerts (Optional)

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Add to Checkly: Settings → Alert Channels
3. Update `checkly/alerts/slack-channel.ts` and uncomment code
4. Redeploy: `npm run checkly:deploy`

## Testing Individual Checks

```bash
# Test specific check
npx checkly test --check rake-health-main

# Test with verbose output
CHECKLY_DEBUG=1 npx checkly test --check dataforge-health-main
```

## Viewing Results

```bash
# List all checks
npx checkly list

# Show account info
npx checkly whoami

# Trigger specific check manually
npx checkly trigger --check vibeforge-login-flow
```

## Common Issues

### "Check not found"
Deploy first: `npm run checkly:deploy`

### "Missing environment variables"
1. Add to Checkly dashboard: Settings → Environment Variables
2. Or export locally: `export RAKE_BASE_URL=https://...`

### Browser check fails
Install Playwright browsers: `npx playwright install --with-deps chromium`

## File Structure

```
checkly/
├── api/                  # Health checks (7 checks)
├── browser/              # Login flows (1 check)
├── alerts/               # Alert configurations
├── __checks__/           # Shared utilities
├── QUICK_START.md       # This file
├── SETUP_GUIDE.md       # Detailed setup
├── README.md            # Full documentation
├── API_REFERENCE.md     # API usage
└── test-local.sh        # Test helper script
```

## Costs

**Your Current Setup:**
- ~43,400 check runs/month
- Free tier: 10,000 runs/month
- **Required plan:** $7/month (100,000 runs)

**To Reduce (fit in free tier):**
- Change critical checks: 5min → 10min (saves 50%)
- Use 1 location instead of 2 (saves 50%)
- Combined: ~10,850 runs/month (fits free tier!)

## Support

- **Full Setup Guide:** `checkly/SETUP_GUIDE.md`
- **Complete Docs:** `checkly/README.md`
- **API Reference:** `checkly/API_REFERENCE.md`
- **Checkly Docs:** https://www.checklyhq.com/docs/

---

**Ready to go!** Start with `./checkly/test-local.sh` 🚀
