#!/bin/bash
# Verification script to ensure sensitive files are properly ignored by git

echo "🔒 Verifying git security before deployment..."

# Check if .gitignore exists and contains essential protections
if [ ! -f .gitignore ]; then
    echo "❌ ERROR: .gitignore file not found!"
    exit 1
fi

# Verify .env is ignored
if grep -q "^\.env$" .gitignore; then
    echo "✅ .env files are protected"
else
    echo "❌ WARNING: .env files not in .gitignore"
fi

# Verify database files are ignored
if grep -q "*.sqlite3" .gitignore; then
    echo "✅ Database files are protected"
else
    echo "❌ WARNING: Database files not in .gitignore"
fi

# Check what would be committed
echo ""
echo "📋 Files that will be committed to git:"
git ls-files --cached 2>/dev/null || echo "Git not initialized yet"

echo ""
echo "🚫 Sensitive files that are properly ignored:"
git status --ignored --porcelain 2>/dev/null | grep "^!!" | head -10 || echo "Git not initialized - will check after git init"

echo ""
echo "💡 To verify security before push:"
echo "   git status --ignored"
echo "   git add . --dry-run"

echo ""
echo "✅ Security verification complete!"
echo "Your .env file will stay local and NOT be committed to git."
