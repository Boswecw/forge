# Checkly API Quick Reference

## Authentication

All Checkly API requests require two headers:

```bash
Authorization: Bearer [YOUR_API_KEY]
X-Checkly-Account: [YOUR_ACCOUNT_ID]
```

## Example API Calls

### Get All Checks

```bash
curl -H "Authorization: Bearer cu_xxx" \
     -H "X-Checkly-Account: xxx" \
     https://api.checklyhq.com/v1/checks
```

### Get Specific Check

```bash
curl -H "Authorization: Bearer cu_xxx" \
     -H "X-Checkly-Account: xxx" \
     https://api.checklyhq.com/v1/checks/[CHECK_ID]
```

### Trigger Check Manually

```bash
curl -X POST \
     -H "Authorization: Bearer cu_xxx" \
     -H "X-Checkly-Account: xxx" \
     https://api.checklyhq.com/v1/checks/[CHECK_ID]/trigger
```

### Get Check Results

```bash
curl -H "Authorization: Bearer cu_xxx" \
     -H "X-Checkly-Account: xxx" \
     https://api.checklyhq.com/v1/check-results?checkId=[CHECK_ID]&limit=10
```

## Using with Checkly CLI

The CLI uses these credentials from environment variables:

```bash
export CHECKLY_API_KEY="cu_xxx"
export CHECKLY_ACCOUNT_ID="xxx"

# Now you can run CLI commands
npx checkly test
npx checkly deploy
npx checkly whoami
```

## Finding Your Credentials

1. Log into [Checkly Dashboard](https://app.checklyhq.com/)
2. Go to **Settings → Account Settings**
3. Click **API Keys** tab
4. Your **Account ID** is shown at the top
5. Click **Create API Key** to generate a new key

## API Documentation

Full API reference: https://www.checklyhq.com/docs/api/

## Common CLI Commands

```bash
# Test checks locally
checkly test

# Test specific check
checkly test --check rake-health-main

# Deploy all checks
checkly deploy

# Deploy with force update
checkly deploy --force

# List all checks
checkly list

# Show account info
checkly whoami

# Trigger specific check
checkly trigger --check rake-health-main

# View check results
checkly results --check rake-health-main
```

## Environment Variables for CI/CD

Set these in GitHub Actions secrets:

```yaml
env:
  CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
  CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
```

## Webhook Signature Verification

When receiving webhooks from Checkly, verify the signature:

```javascript
const crypto = require('crypto')

function verifyChecklySignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret)
  hmac.update(payload)
  const calculatedSignature = hmac.digest('hex')
  return signature === calculatedSignature
}

// In your webhook handler
app.post('/webhook/checkly', (req, res) => {
  const signature = req.headers['x-checkly-signature']
  const isValid = verifyChecklySignature(
    JSON.stringify(req.body),
    signature,
    process.env.CHECKLY_WEBHOOK_SECRET
  )

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' })
  }

  // Process webhook
  console.log('Check result:', req.body)
  res.status(200).json({ received: true })
})
```

## Rate Limits

- **API Rate Limit**: 100 requests per minute
- **CLI Rate Limit**: No limit for authenticated users
- **Check Runs**: Based on your plan (10,000/month free tier)

## Support

- **API Issues**: Check [Checkly Status](https://status.checklyhq.com/)
- **Documentation**: https://www.checklyhq.com/docs/
- **Support**: support@checklyhq.com
