#!/bin/bash

echo "🚀 Starting git operations..."

# Add all the cache busting files and changes
echo "📁 Adding files to git..."
git add frontend/build-timestamp.txt
git add frontend/version.txt
git add frontend/Dockerfile
git add frontend/package.json
git add frontend/.dockerignore
git add backend/Dockerfile
git add render.yaml
git add frontend/src/pages/AboutPage.tsx
git add commit_and_push.sh
git add commit_changes.sh
git add execute_git.sh
git add push_all_changes.sh

echo "✅ Files added successfully!"

# Commit with detailed message
echo "📝 Committing changes..."
git commit -m "Force complete rebuild: Add cache busting, build timestamps, and version tracking to fix deployment issues

- Added cache busting arguments to both Dockerfiles
- Created build timestamp and version files
- Updated render.yaml with build commands
- Added prebuild/postbuild scripts to package.json
- Added .dockerignore for frontend
- Verified phone number removal from AboutPage
- All changes to force fresh Docker builds on Render"

echo "✅ Commit successful!"

# Push to main branch
echo "🚀 Pushing to main branch..."
git push origin main

echo "✅ SUCCESS! All changes pushed to remote repository!"
echo "📋 Check Render dashboard for deployment progress."
echo "🔄 The deployment should now include all your latest changes."
echo "📱 Phone number should be removed from About page after deployment."
