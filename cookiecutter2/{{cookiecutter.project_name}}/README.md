## {{cookiecutter.project_name}}

### Overview
#### {{cookiecutter.description}}

Created with cookiecutter2 template: "https://github.com/essans/templates/tree/main/cookiecutter2"

### Environment set-up
Using pip and virtualenv
```bash
# Activate your default environment
python -m venv ~/environments/venv #if default environment not set up
source ~/environments/venv/bin/activate

# Create project specific virtual environment
python -m venv {{cookiecutter.project_name}}_env
source {{cookiecutter.project_name}}_env/bin/activate

# windows use:
{{cookiecutter.project_name}}_env\Scripts\activate 
```
<br>

### Install the project in editable mode so console scripts and imports always point to your local source tree.
```
pip install -e .
pip install -e ".[dev]" # if dev extra is defined
```

# if need to upgrade later
```
pip install -e . --upgrade
pip install -e ".[dev]" --upgrade

#or more aggressively pip install -e . --force-reinstall

```

### Use this instead if the project exposes a dev extra for tooling/test deps.
```
pip install -e .[dev]
```

`deactivate` #when done


_Editable installs make sure any changes made in the repository are instantly reflected when you run the package or its console scripts, and the `.[dev]` extra (if defined) bundles linting, testing, and other tooling dependencies needed for local development._


### Dependencies
```
pip install -r requirements.txt
```

### Usage
```bash
chmod +x /scripts/*
```
<br>

### Structure

```
{{cookiecutter.project_name}}/
|
├── .vscode/
│   └── settings.json
|
├── configs/
│   └── settings.yaml
|
├── data/
│   ├── raw/
│   └── processed/
|
├── notebooks/
│   └── {{cookiecutter.project_name}}.ipynb
|
├── outputs/
│   └── logs/
|
├── scripts/
|
├── src/
│   └── __init__.py
|
├── .env
├── README.md
├── pyproject.toml
└── requirements.txt
```

`.env` sets `PYTHONPATH` for tooling, `.vscode/settings.json` ships workspace defaults (formatting, terminals, etc.), and `pyproject.toml` captures the project metadata plus runtime/dev dependencies for editable installs.


### Create git remote and local repo
```bash
gh auth status
gh auth switch --user <your-gh-username>

# gh repo list #--source #--limit

# git config user.name  "myName"
# git config user.email "myName@domain.com" 

gh repo create {{cookiecutter.project_name}} --private

git init

git add . #git add README.md

git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:<org-or-user>/{{cookiecutter.project_name}}.git
git push -u origin main
```

#### If remote needs to be updated then:
```bash
git remote -v # show remotes
git remote remove origin # in case need to remove (then git remote add origin <new-url>)

# or
git remote set-url origin git@github.com:essans/{{cookiecutter.project_name}}.git # in case to update URL

#then as before
git push -u origin main
```
