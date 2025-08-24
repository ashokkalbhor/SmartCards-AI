#!/bin/bash

echo "Adding all changes to git..."

# Add all the new and modified files
git add frontend/build-timestamp.txt
git add frontend/version.txt
git add frontend/Dockerfile
git add frontend/package.json
git add frontend/.dockerignore
git add backend/Dockerfile
git add render.yaml
git add frontend/src/pages/AboutPage.tsx
git add commit_and_push.sh

echo "Committing changes..."

# Commit with a descriptive message
git commit -m "Force complete rebuild: Add cache busting, build timestamps, and version tracking to fix deployment issues

- Added cache busting arguments to both Dockerfiles
- Created build timestamp and version files
- Updated render.yaml with build commands
- Added prebuild/postbuild scripts to package.json
- Added .dockerignore for frontend
- Verified phone number removal from AboutPage
- All changes to force fresh Docker builds on Render"

echo "Pushing to main branch..."

# Push to main branch
git push origin main

echo "✅ Changes committed and pushed successfully!"
echo "📋 Check Render dashboard for deployment progress."
echo "🔄 The deployment should now include all your latest changes."
