#!/bin/bash

# Security verification script for Kapiga Research Site
# Run this before deploying to check for any security issues

echo "🔒 Running Security Verification for Kapiga Research Site..."
echo "============================================================"

# Check if .env is properly ignored
echo "1. Checking if .env is ignored by git..."
if git check-ignore .env >/dev/null 2>&1; then
    echo "✅ .env is properly ignored by git"
else
    echo "❌ WARNING: .env is NOT ignored by git!"
    echo "   Run: git rm --cached .env"
fi

# Check for any secrets in tracked files
echo ""
echo "2. Checking for potential secrets in tracked files..."
SECRETS_FOUND=$(git ls-files | xargs grep -l "password\|secret\|key" 2>/dev/null | grep -v ".gitignore\|requirements.txt\|README.md\|SECURITY.md" || true)

if [ -z "$SECRETS_FOUND" ]; then
    echo "✅ No obvious secrets found in tracked files"
else
    echo "❌ WARNING: Potential secrets found in tracked files:"
    echo "$SECRETS_FOUND"
    echo "   Review these files for hardcoded credentials"
fi

# Check if SECRET_KEY is using environment variables
echo ""
echo "3. Checking Django settings for hardcoded secrets..."
if grep -q "SECRET_KEY.*os.environ.get\|SECRET_KEY.*config" django_project/kapiga_site/settings.py; then
    echo "✅ SECRET_KEY is using environment variables"
else
    echo "❌ WARNING: SECRET_KEY appears to be hardcoded in settings.py"
fi

# Check docker-compose for hardcoded passwords
echo ""
echo "4. Checking docker-compose for hardcoded credentials..."
if grep -q "POSTGRES_PASSWORD.*\${" docker-compose.yml; then
    echo "✅ Docker compose is using environment variables"
else
    echo "❌ WARNING: Docker compose may have hardcoded credentials"
fi

# Check if required environment variables are set
echo ""
echo "5. Checking if .env file has required variables..."
REQUIRED_VARS=("SECRET_KEY" "POSTGRES_PASSWORD" "ALLOWED_HOSTS")
for var in "${REQUIRED_VARS[@]}"; do
    if grep -q "^$var=" .env 2>/dev/null; then
        if grep -q "^$var=CHANGE-ME\|^$var=your-" .env; then
            echo "⚠️  $var is set but needs to be updated with real value"
        else
            echo "✅ $var is set"
        fi
    else
        echo "❌ $var is missing from .env file"
    fi
done

# Check git status
echo ""
echo "6. Current git status:"
git status --porcelain

echo ""
echo "============================================================"
echo "🔒 Security verification complete!"
echo ""
echo "NEXT STEPS:"
echo "1. Generate a new SECRET_KEY: cd django_project && python manage.py shell -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo "2. Update .env with secure values"
echo "3. Set DEBUG=False for production"
echo "4. Configure proper ALLOWED_HOSTS for your domain"
echo "5. Set up SSL certificates in ./ssl/ directory"
echo "6. Test with: docker-compose -f docker-compose.production.yml up"
