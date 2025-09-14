# 🌳 GitFlow Workflow Documentation

## Overview

This repository uses GitFlow, a branching model that provides a robust framework for managing feature development, releases, and hotfixes. GitFlow ensures code quality, enables parallel development, and maintains a stable production branch.

## 🌳 Branch Structure

- **`main`**: Production-ready code (stable releases)
- **`develop`**: Integration branch for features (development)
- **`feature/*`**: New features and enhancements
- **`release/*`**: Preparing releases (version bumping, final testing)
- **`hotfix/*`**: Critical production fixes (bypasses develop)

## 🔄 Workflow

### Feature Development

1. **Start a new feature:**
   ```bash
   git flow feature start feature-name
   # This creates: feature/feature-name from develop
   ```

2. **Develop and commit changes:**
   ```bash
   git add .
   git commit -m "feat(feature-name): add new functionality"
   ```

3. **Finish the feature:**
   ```bash
   git flow feature finish feature-name
   # This merges feature/feature-name into develop and deletes the feature branch
   ```

4. **Push develop branch:**
   ```bash
   git push origin develop
   ```

### Release Process

1. **Start a release:**
   ```bash
   git flow release start 1.0.0
   # This creates: release/1.0.0 from develop
   ```

2. **Update version numbers, changelog, etc.**
   ```bash
   git commit -m "chore(release): bump version to 1.0.0"
   ```

3. **Finish the release:**
   ```bash
   git flow release finish 1.0.0
   # This merges release/1.0.0 into main and develop, creates a tag
   ```

4. **Push tags and branches:**
   ```bash
   git push origin --tags
   git push origin main develop
   ```

### Hotfix Process

1. **Start a hotfix:**
   ```bash
   git flow hotfix start 1.0.1
   # This creates: hotfix/1.0.1 from main
   ```

2. **Fix critical issues:**
   ```bash
   git commit -m "fix(critical): resolve production issue"
   ```

3. **Finish the hotfix:**
   ```bash
   git flow hotfix finish 1.0.1
   # This merges hotfix/1.0.1 into main and develop, creates a tag
   ```

4. **Deploy immediately:**
   ```bash
   git push origin --tags
   git push origin main develop
   ```

## 📝 Commit Message Format

We use the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer(s)]
```

### Types:
- **`feat`**: A new feature
- **`fix`**: A bug fix
- **`docs`**: Documentation only changes
- **`style`**: Changes that do not affect the meaning of the code
- **`refactor`**: A code change that neither fixes a bug nor adds a feature
- **`test`**: Adding missing tests or correcting existing tests
- **`chore`**: Changes to the build process or auxiliary tools
- **`perf`**: A code change that improves performance
- **`ci`**: Changes to CI configuration files and scripts
- **`build`**: Changes that affect the build system or external dependencies
- **`revert`**: Reverts a previous commit

### Examples:
```bash
feat(auth): add user authentication system
fix(api): resolve database connection timeout
docs(readme): update installation instructions
style(ui): format code according to style guide
refactor(models): simplify user model structure
test(api): add unit tests for authentication
chore(deps): update dependencies to latest versions
perf(db): optimize database queries
ci(github): add automated testing workflow
build(docker): update Docker configuration
```

## 🛡️ Branch Protection Rules

- **Main branch**: Requires PR reviews, status checks must pass
- **Develop branch**: Requires PR reviews, status checks must pass
- **Feature branches**: Must be merged via pull request
- **Release branches**: Must be merged into both main and develop
- **Hotfix branches**: Must be merged into both main and develop

## 🔍 Automated Checks

Our GitHub Actions workflow automatically:

- ✅ Validates branch naming conventions
- ✅ Checks commit message format
- ✅ Scans for secrets and sensitive data
- ✅ Runs code quality checks (flake8, black, isort)
- ✅ Tests Docker build process
- ✅ Validates Docker Compose configuration

## 🚀 Quick Start

1. **Install git-flow:**
   ```bash
   # macOS
   brew install git-flow
   
   # Ubuntu/Debian
   sudo apt-get install git-flow
   
   # Windows
   # Download from: https://github.com/nvie/gitflow
   ```

2. **Initialize GitFlow in your repository:**
   ```bash
   ./scripts/setup-gitflow.sh
   ```

3. **Start developing:**
   ```bash
   git flow feature start my-new-feature
   # Make changes, commit, then:
   git flow feature finish my-new-feature
   ```

## 📋 Best Practices

### Do's ✅
- Always start features from `develop`
- Use descriptive branch names: `feature/user-authentication`
- Write clear, conventional commit messages
- Test your changes before finishing features
- Keep feature branches small and focused
- Update documentation for new features

### Don'ts ❌
- Don't commit directly to `main` or `develop`
- Don't merge feature branches into `main`
- Don't use generic commit messages like "fix stuff"
- Don't commit secrets or sensitive data
- Don't leave feature branches open indefinitely
- Don't skip testing before merging

## 🔧 Troubleshooting

### Common Issues:

**Q: "git-flow command not found"**
A: Install git-flow using your package manager (see Quick Start section)

**Q: "Branch protection rule prevents push"**
A: Create a pull request instead of pushing directly

**Q: "Commit message format validation failed"**
A: Use conventional commit format: `type(scope): description`

**Q: "Security scan failed"**
A: Remove any hardcoded secrets, passwords, or API keys from your code

### Getting Help:

1. Check the [GitFlow documentation](https://nvie.com/posts/a-successful-git-branching-model/)
2. Review the [Conventional Commits specification](https://www.conventionalcommits.org/)
3. Check GitHub Actions logs for detailed error messages
4. Ask team members for assistance

## 📊 Branch Naming Conventions

- **Features**: `feature/description` (e.g., `feature/user-authentication`)
- **Releases**: `release/version` (e.g., `release/1.0.0`)
- **Hotfixes**: `hotfix/version` (e.g., `hotfix/1.0.1`)
- **Support**: `support/description` (e.g., `support/legacy-api`)

## 🎯 Integration with Research Platform

This GitFlow setup is specifically configured for the Dr. Saidi Kapiga HIV Research Platform:

- **Feature branches** for new research analysis tools
- **Release branches** for research data updates
- **Hotfix branches** for critical security or data integrity issues
- **Automated security scanning** for HIPAA/GDPR compliance
- **Database migration validation** for research data integrity

---

**Happy coding! 🚀**

For questions or issues with this workflow, please create an issue using the GitHub issue templates.
