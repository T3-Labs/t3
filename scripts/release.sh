#!/usr/bin/env bash
# Release script for T3 CLI

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if version is provided
if [ -z "$1" ]; then
    print_error "Usage: $0 <version>"
    echo "Example: $0 0.2.0"
    exit 1
fi

VERSION=$1
VERSION_TAG="v${VERSION}"

print_info "Starting release process for version ${VERSION}"

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Invalid version format. Use: MAJOR.MINOR.PATCH (e.g., 0.2.0)"
    exit 1
fi

# Check if on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "You are not on main branch (current: ${CURRENT_BRANCH})"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_error "You have uncommitted changes. Please commit or stash them first."
    exit 1
fi

# Pull latest changes
print_info "Pulling latest changes..."
git pull origin main

# Update version in pyproject.toml
print_info "Updating version in pyproject.toml..."
sed -i "s/^version = \".*\"/version = \"${VERSION}\"/" pyproject.toml
print_success "Version updated to ${VERSION}"

# Show git diff
print_info "Changes to be committed:"
git diff pyproject.toml

# Confirm
read -p "Commit these changes? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    git restore pyproject.toml
    print_warning "Release cancelled"
    exit 1
fi

# Commit version bump
print_info "Committing version bump..."
git add pyproject.toml
git commit -m "chore: bump version to ${VERSION}"
print_success "Version committed"

# Push changes
print_info "Pushing changes to main..."
git push origin main
print_success "Changes pushed"

# Create tag
print_info "Creating tag ${VERSION_TAG}..."
git tag -a "${VERSION_TAG}" -m "Release ${VERSION_TAG}"
print_success "Tag created"

# Push tag
print_info "Pushing tag..."
git push origin "${VERSION_TAG}"
print_success "Tag pushed"

# Print next steps
echo ""
print_success "Release process completed successfully!"
echo ""
print_info "Next steps:"
echo "1. Go to: https://github.com/T3-Labs/t3/releases/new"
echo "2. Select tag: ${VERSION_TAG}"
echo "3. Title: ${VERSION_TAG} - <Release Name>"
echo "4. Add release notes (see CHANGELOG in README.md)"
echo "5. Click 'Publish release'"
echo ""
print_info "The CI/CD pipeline will automatically:"
echo "  - Run tests"
echo "  - Build package"
echo "  - Publish to PyPI"
echo ""
print_info "Monitor the workflow at:"
echo "https://github.com/T3-Labs/t3/actions"
