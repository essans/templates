#!/bin/bash

# GitHub CLI is required for this template's automation, so verify it before doing anything else
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install it from https://cli.github.com/ and re-run 'cookiecutter' once it's available."
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "Error: GitHub CLI (gh) is installed but not authenticated."
    echo "Run 'gh auth login' to authenticate, then re-run 'cookiecutter' to generate the project."
    exit 1
fi

# Always initialize the local git repository
git init
git add .
git commit -m "Initial commit from cookiecutter template"

# Capture the user's choice and convert it to lowercase for easier matching
CREATE_REPO="{{ cookiecutter.create_gh_repo | lower }}"

# Check if the user entered 'y' or 'yes'
if [[ "$CREATE_REPO" == "y" || "$CREATE_REPO" == "yes" ]]; then
    echo "Creating GitHub repository..."
    # Using project_name for the repo name here, adjust if needed
    gh repo create "{{ cookiecutter.project_name }}" --private --source=. --remote=origin --push
    echo "Successfully created and pushed to GitHub!"
else
    echo "Local repository initialized. Skipping GitHub creation as requested."
fi
