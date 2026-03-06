#!/bin/bash
# Quick script to test Checkly checks locally

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checkly Local Test Runner${NC}"
echo ""

# Load environment variables
if [ -f "../.env.checkly" ]; then
    echo -e "${GREEN}✓ Loading credentials from .env.checkly${NC}"
    set -a
    source ../.env.checkly
    set +a
else
    echo -e "${RED}✗ .env.checkly not found!${NC}"
    echo "  Please copy .env.checkly.example to .env.checkly and configure it"
    exit 1
fi

# Check required variables
if [ -z "$CHECKLY_API_KEY" ] || [ -z "$CHECKLY_ACCOUNT_ID" ]; then
    echo -e "${RED}✗ Missing CHECKLY_API_KEY or CHECKLY_ACCOUNT_ID${NC}"
    exit 1
fi

echo -e "${GREEN}✓ API Key: ${CHECKLY_API_KEY:0:10}...${NC}"
echo -e "${GREEN}✓ Account ID: $CHECKLY_ACCOUNT_ID${NC}"
echo ""

# Run tests
echo -e "${YELLOW}Running Checkly tests...${NC}"
echo ""

cd ..
npm run checkly:test

echo ""
echo -e "${GREEN}✓ Tests complete!${NC}"
