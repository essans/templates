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

### Dependencies (esp. when not using an isolated enviroment
```
pip install -r requirements.txt
```

### Usage
```bash
chmod +x /scripts/*
```

### Structure

```
ROOT
├── cookiecutter.json
|
├── hooks
│   ├── post_gen_project.py
│   └── pre_gen_project.py
|
└── {{cookiecutter.project_name}}
    ├── README.md
    |
    ├── configs
    │   └── config.yaml
    |
    ├── data
    │   ├── processed
    │   ├── processed_sample
    │   ├── raw
    │   └── raw_sample
    |
    ├── environment.yml
    |
    ├── models
    │   └── checkpoints
    |
    ├── notebooks
    |
    ├── outputs
    │   ├── logs
    │   ├── metrics
    │   ├── predictions
    │   └── visualizations
    |
    ├── requirements.txt
    |
    ├── scripts
    │   ├── predict.py
    │   └── train.py
    |
    ├── setup.py
    ├── src
    │   └── __init__.py
    |
    └── tests
```

20 directories, 11 files



### Note to self for potential further enhancements:
https://github.com/drivendataorg/cookiecutter-data-science/
https://medium.com/data-science-deep-dive/data-science-cookiecutter-ca8a94546539

