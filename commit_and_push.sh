#!/bin/bash

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "Force complete rebuild: Add cache busting, build timestamps, and version tracking to fix deployment issues"

# Push to main branch
git push origin main

echo "Changes committed and pushed successfully!"
echo "Check Render dashboard for deployment progress."
