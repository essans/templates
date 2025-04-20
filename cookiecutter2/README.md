### cookiecutter1 
 - bare bones

<br> 

#### option1: clone from local cookiecutter:
(1) clone to local<br>
(2) from location where new project is to be created:
```
cookiecutter /path/to/cookiecutter_local_repo/cookiecutter1
```

#### option2: create new project based on remote github cookiecutter:
```
cookiecutter git@github:/essans/template.git --directory cookiecutter1 -c main

cookiecutter git@github:/essans/template.git --directory cookiecutter1 -c branchname
```
