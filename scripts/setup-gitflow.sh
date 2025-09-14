#!/bin/bash

echo "🔧 Setting up GitFlow for Dr. Saidi Kapiga Research Platform..."

# Check if git-flow is installed
if ! command -v git-flow &> /dev/null; then
    echo "❌ git-flow is not installed. Please install it first:"
    echo "   macOS: brew install git-flow"
    echo "   Ubuntu: apt-get install git-flow"
    echo "   Windows: Download from https://github.com/nvie/gitflow"
    exit 1
fi

# Initialize git-flow
echo "🚀 Initializing GitFlow..."
git flow init -d

# Create develop branch if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo "📝 Creating develop branch..."
    git checkout -b develop
    git push -u origin develop
fi

# Set up branch protection rules (requires GitHub CLI)
if command -v gh &> /dev/null; then
    echo "🛡️ Setting up branch protection rules..."
    
    # Get repository info
    REPO_OWNER=$(gh repo view --json owner --jq '.owner.login')
    REPO_NAME=$(gh repo view --json name --jq '.name')
    
    # Protect main branch
    gh api repos/$REPO_OWNER/$REPO_NAME/branches/main/protection \
        --method PUT \
        --field required_status_checks='{"strict":true,"contexts":["GitFlow Enforcement"]}' \
        --field enforce_admins=true \
        --field required_pull_request_reviews='{"required_approving_review_count":1}' \
        --field restrictions='{"users":[],"teams":[]}' || echo "⚠️ Could not set branch protection (may need admin access)"
    
    # Protect develop branch
    gh api repos/$REPO_OWNER/$REPO_NAME/branches/develop/protection \
        --method PUT \
        --field required_status_checks='{"strict":true,"contexts":["GitFlow Enforcement"]}' \
        --field enforce_admins=true \
        --field required_pull_request_reviews='{"required_approving_review_count":1}' \
        --field restrictions='{"users":[],"teams":[]}' || echo "⚠️ Could not set branch protection (may need admin access)"
else
    echo "⚠️ GitHub CLI not found. Please set up branch protection rules manually:"
    echo "   1. Go to GitHub repository settings"
    echo "   2. Navigate to Branches"
    echo "   3. Add rule for 'main' branch"
    echo "   4. Add rule for 'develop' branch"
fi

echo "✅ GitFlow setup complete!"
echo ""
echo "🌳 GitFlow Commands:"
echo "   Feature:  git flow feature start <name>"
echo "   Release:  git flow release start <version>"
echo "   Hotfix:   git flow hotfix start <version>"
echo ""
echo "🔄 Workflow:"
echo "   1. Start feature: git flow feature start <name>"
echo "   2. Develop and commit changes"
echo "   3. Finish feature: git flow feature finish <name>"
echo "   4. Push develop: git push origin develop"
echo "   5. Create PR: develop → main (for releases)"
echo ""
echo "📝 Commit Message Format:"
echo "   feat(scope): description"
echo "   fix(scope): description"
echo "   docs(scope): description"
