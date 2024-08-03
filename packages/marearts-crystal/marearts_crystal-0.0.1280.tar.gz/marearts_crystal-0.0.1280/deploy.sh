#!/bin/bash

# Function to update version in a file
update_version() {
    local file=$1
    local new_version=$2
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/version = .*/version = \"$new_version\"/" "$file"
    else
        # Linux and others
        sed -i "s/version = .*/version = \"$new_version\"/" "$file"
    fi
}

# Get current version
CURRENT_VERSION=$(grep "version = " setup.cfg | cut -d'"' -f2)
echo "Current version: $CURRENT_VERSION"

# Prompt for new version
read -p "Enter the new version number: " NEW_VERSION

# Update version in setup.cfg
update_version "setup.cfg" "$NEW_VERSION"

# Update version in pyproject.toml if it exists
if [ -f "pyproject.toml" ]; then
    update_version "pyproject.toml" "$NEW_VERSION"
fi

# Commit all changes
git add .
git commit -m "Bump version to $NEW_VERSION"

# Create and push tag
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
git push origin main "v$NEW_VERSION"

echo "Deployment process completed. GitHub Actions should now build and publish version $NEW_VERSION."