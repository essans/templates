#!/bin/bash

# GitHub CLI is required for this template's automation, so verify it before doing anything else
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install it from https://cli.github.com/ and re-run 'cookiecutter' once it's available."
    exit 1
fi

# 'gh auth status' fails if ANY stored account has a bad token, so check the active account via an API call
if ! gh api user --silent &> /dev/null; then
    echo "Error: GitHub CLI (gh) is installed but not authenticated."
    echo "Run 'gh auth login' to authenticate, then re-run 'cookiecutter' to generate the project."
    exit 1
fi

# Create and activate a virtual environment in ~/environments/ if a name was provided
VENV_NAME="{{ cookiecutter.venv_name | trim }}"
VENV_STATUS=""
if [[ -n "$VENV_NAME" ]]; then
    VENV_PATH="$HOME/environments/$VENV_NAME"

    if [[ -f "$VENV_PATH/bin/activate" ]]; then
        VENV_STATUS="exists"
    else
        PY_BIN="python{{ cookiecutter.python_version }}"
        if ! command -v "$PY_BIN" &> /dev/null; then
            echo "Warning: $PY_BIN not found, falling back to python3."
            PY_BIN="python3"
        fi
        mkdir -p "$HOME/environments"
        "$PY_BIN" -m venv "$VENV_PATH" || { echo "Error: failed to create venv at $VENV_PATH"; exit 1; }
        VENV_STATUS="created"
    fi

    # Activate for the rest of this hook (installs go into the venv)
    source "$VENV_PATH/bin/activate"
    INSTALL_DEPS="{{ cookiecutter.install_dependencies | lower }}"
    if [[ "$INSTALL_DEPS" == "y" || "$INSTALL_DEPS" == "yes" ]]; then
        if [[ "$VENV_STATUS" == "created" ]]; then
            pip install --upgrade pip
        fi
        pip install -e ".[dev]" || echo "Warning: editable install failed; install dependencies manually."
    else
        echo "Skipping pip install as requested."
    fi
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

# Final venv summary
if [[ "$VENV_STATUS" == "created" ]]; then
    echo "Virtual environment '$VENV_NAME' was created at $VENV_PATH"
elif [[ "$VENV_STATUS" == "exists" ]]; then
    echo "Virtual environment '$VENV_NAME' already exists at $VENV_PATH (not recreated, just activated for setup)"
fi
if [[ -n "$VENV_STATUS" ]]; then
    # A hook runs in a subprocess, so it cannot activate the venv in your terminal
    echo "To activate it in your shell, run:"
    echo "    source $VENV_PATH/bin/activate"
fi
