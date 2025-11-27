## {{cookiecutter.project_name}}

### Overview
#### {{cookiecutter.description}}

Created with cookiecutter2 template: "https://github.com/{{cookiecutter.username}}/templates/tree/main/cookiecutter2"

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
