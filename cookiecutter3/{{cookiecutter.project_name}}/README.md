## {{cookiecutter.project_name}}

### Overview
#### {{cookiecutter.description}}

### Environment set-up
Using pip
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
cd src
streamlit run app.py
```

### Structure

```

```
