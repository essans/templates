### cookiecutter5
 - Essentially extends cookiecutter3 and includes first attempt at better organization for src

<br> 

#### option1: clone from local cookiecutter:
(1) clone to local<br>
(2) from location where new project is to be created:
```
cookiecutter /path/to/cookiecutter_local_repo/cookiecutter5
```

#### option2: create new project based on remote bbgithub cookiecutter:
```
cookiecutter git@github:/essans/template.git --directory cookiecutter5 -c main

cookiecutter git@github:/essans/template.git --directory cookiecutter5 -c branchname
```
