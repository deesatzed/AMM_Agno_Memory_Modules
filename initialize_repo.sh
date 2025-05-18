#!/bin/bash

# Initialize Git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Core AMM Agno Memory Modules"

echo ""
echo "Repository initialized successfully!"
echo "To connect to a new GitHub repository, run the following commands:"
echo ""
echo "# Create a new repository on GitHub"
echo "# Then add the remote and push:"
echo "git remote add origin <your-github-repo-url>"
echo "git branch -M main"
echo "git push -u origin main"
echo ""

# Make the script executable
chmod +x initialize_repo.sh
