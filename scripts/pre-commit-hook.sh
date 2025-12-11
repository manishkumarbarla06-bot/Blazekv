# Pre-commit hook to prevent accidental secret commits
# Copy this file to .git/hooks/pre-commit and make it executable

#!/bin/bash
# BlazeKV Pre-commit Security Hook
# Prevents common secrets from being committed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# List of patterns to check
SECRETS=(
    # API Keys and Tokens
    "api[_-]?key"
    "apikey"
    "access[_-]?token"
    "auth[_-]?token"
    "authentication[_-]?token"
    "personal[_-]?access[_-]?token"
    "github[_-]?token"
    "gitlab[_-]?token"
    "bitbucket[_-]?token"
    
    # AWS Credentials
    "aws[_-]?access[_-]?key"
    "aws[_-]?secret[_-]?key"
    "aws_access_key_id"
    "aws_secret_access_key"
    
    # Database Credentials
    "password"
    "passwd"
    "pwd"
    "database[_-]?password"
    "db[_-]?password"
    "mongo[_-]?url"
    
    # Private Keys
    "private[_-]?key"
    "private[_-]?pem"
    "begin rsa private key"
    "begin openssh private key"
    
    # OAuth/Client Secrets
    "client[_-]?secret"
    "oauth[_-]?token"
    "oauth[_-]?secret"
    
    # Other sensitive data
    "secret"
    "secret[_-]?key"
    "encryption[_-]?key"
)

# Files to exclude from scanning
EXCLUDE_PATTERNS=(
    "\.git/"
    "\.gitignore"
    "node_modules/"
    "\.env\.example"
    "SECURITY\.md"
)

echo -e "${GREEN}[Pre-commit Hook]${NC} Running security checks..."

FOUND_SECRETS=0

# Check staged changes
while IFS= read -r file; do
    # Skip excluded patterns
    SKIP=0
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ $file =~ $pattern ]]; then
            SKIP=1
            break
        fi
    done
    
    if [ $SKIP -eq 1 ]; then
        continue
    fi
    
    # Check for secrets in staged content
    for secret_pattern in "${SECRETS[@]}"; do
        if git diff --cached "$file" | grep -iE "^\+.*$secret_pattern.*=" > /dev/null; then
            echo -e "${RED}[SECURITY WARNING]${NC} Potential secret found in: $file"
            echo "  Pattern: $secret_pattern"
            echo ""
            FOUND_SECRETS=$((FOUND_SECRETS + 1))
        fi
    done
done < <(git diff --cached --name-only)

# Check for .env files
if git diff --cached --name-only | grep -E '\.env($|\.)' > /dev/null; then
    echo -e "${RED}[SECURITY WARNING]${NC} .env file detected in commit"
    echo "  .env files should never be committed"
    FOUND_SECRETS=$((FOUND_SECRETS + 1))
fi

# Check for common credential files
CREDENTIAL_FILES=(
    "credentials.json"
    "credentials.txt"
    "secrets.json"
    "secrets.txt"
    "id_rsa"
    "id_ed25519"
    "\.pem$"
    "\.key$"
)

for file in "${CREDENTIAL_FILES[@]}"; do
    if git diff --cached --name-only | grep -E "$file" > /dev/null; then
        echo -e "${RED}[SECURITY WARNING]${NC} Credential file detected: $file"
        FOUND_SECRETS=$((FOUND_SECRETS + 1))
    fi
done

# Result
if [ $FOUND_SECRETS -gt 0 ]; then
    echo ""
    echo -e "${RED}[COMMIT BLOCKED]${NC} Found $FOUND_SECRETS potential security issue(s)"
    echo ""
    echo "To proceed despite warnings (not recommended):"
    echo "  git commit --no-verify"
    echo ""
    echo "To unstage files:"
    echo "  git reset HEAD <file>"
    echo ""
    exit 1
else
    echo -e "${GREEN}[OK]${NC} No obvious secrets detected"
    exit 0
fi
