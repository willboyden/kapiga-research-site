#!/bin/bash
# Quick cleanup script to prepare for deployment
# Keeps .env locally but ensures it won't be committed

echo "🧹 Preparing for secure deployment..."

# Remove any database files (these will be recreated)
rm -f *.db
rm -f *.sqlite3
rm -f django_project/*.db
rm -f django_project/*.sqlite3

# Remove any log files
rm -f *.log
rm -f django_project/*.log

# Remove any Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Remove any temporary IDE files
rm -rf .vscode/settings.json 2>/dev/null || true
rm -rf .idea 2>/dev/null || true

echo "✅ Cleanup complete!"
echo ""
echo "🔒 Files cleaned (but kept locally):"
echo "  • Database files (will be recreated on Railway)"
echo "  • Log files"
echo "  • Python cache files"
echo "  • Temporary IDE files"
echo ""
echo "📁 Files kept locally:"
echo "  • .env (for local development - protected by .gitignore)"
echo "  • All source code"
echo "  • Configuration files"
echo ""
echo "🚀 Ready for secure git commit and Railway deployment!"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Deploy Dr. Kapiga research platform'"
echo "3. git push origin main"
echo "4. Deploy to Railway"
