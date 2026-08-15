#!/bin/bash

# Initialize the local git repository
git init
git add .
git commit -m "Initial commit from cookiecutter template"

# Ensure the user has the GitHub CLI installed and authenticated
if command -v gh &> /dev/null; then
    # Create the repo on GitHub and push the current directory
    # You can change --private to --public depending on your needs
    gh repo create "{{ cookiecutter.repo_name }}" --private --source=. --remote=origin --push
    echo "Successfully created and pushed to GitHub!"
else
    echo "GitHub CLI (gh) is not installed. Skipping automatic GitHub repo creation."
    echo "You will need to push this repository manually."
fi
