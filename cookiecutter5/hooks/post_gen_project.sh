#!/bin/bash

# Always initialize the local git repository
git init
git add .
git commit -m "Initial commit from cookiecutter template"

# Capture the user's choice and convert it to lowercase for easier matching
CREATE_REPO="{{ cookiecutter.create_gh_repo | lower }}"

# Check if the user entered 'y' or 'yes'
if [[ "$CREATE_REPO" == "y" || "$CREATE_REPO" == "yes" ]]; then
    
    # Ensure the user has the GitHub CLI installed
    if command -v gh &> /dev/null; then
        echo "Creating GitHub repository..."
        # Using project_name for the repo name here, adjust if needed
        gh repo create "{{ cookiecutter.project_name }}" --private --source=. --remote=origin --push
        echo "Successfully created and pushed to GitHub!"
    else
        echo "Warning: GitHub CLI (gh) is not installed. Could not create the remote repository."
        echo "You will need to create it manually and push."
    fi

else
    echo "Local repository initialized. Skipping GitHub creation as requested."
fi
