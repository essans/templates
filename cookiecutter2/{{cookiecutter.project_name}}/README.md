## {{cookiecutter.project_name}}

### Overview
#### {{cookiecutter.description}}

### Environment set-up
Option 1: Using conda
```bash
conda env create -f environment.yml
conda activate {{cookiecutter.project_name}}_env
conda deactive #when done
```

Option 2: Using pip
```bash
python -m venv {{cookiecutter.project_name}}_env
source {{cookiecutter.project_name}}_env/bin/activate
{{cookiecutter.project_name}}_env\Scripts\activate #windows
pip install -r requirements.txt
deactivate #when done
```

### Dependencies
```
pip install -r requirements.txt
```

### Usage
```bash
chmod +x /scripts/*
```

### Structure

```

```
