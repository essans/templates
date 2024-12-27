from setuptools import setup, find_packages

setup(
  name = "{{cookiecutter.project_name}}",
  version = "0.1.0",
  author = "{{cookiecutter.author_name}}",
  description = "{{cookiecutter.description}}",
  package_dir = {"":"src"},
  install_required = [
    #TBD
  ]
)
