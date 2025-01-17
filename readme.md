# Multi-Cookiecutter Repository

This repo contains multiple Cookiecutter templates.

## Available Templates

1. **cookiecutter1**: v1 generic cookiecutter.

   - Bare bones

<br>

## Installation: 

### Option1 -clone from local repo <br>
   (1) clone template repo to local drive <br>
   (2) from location where new project is to be created:<br>
   ```
   cookiecutter /path/to/cookiecutter_local_repo/cookiecutter1  #resplace 1 with n as needed
   ```
   (3) see README.MD in corresponding cookiecutter for additional info/steps
   
<br>

### option2: create new project based on remote bbgithub cookiecutter:
   (1) from location where new project is to be created:<br>
   
   ```
   cookiecutter https://github.com/essans/templates.git --directory cookiecutter1

   or

   cookiecutter git@github.com:essans/templates.git --directory cookiecutter1
   ```

if testing from a specific branch then:
   ```
   cookiecutter git@github.com:essans/templates.git --directory cookiecutter1 -c branchname
   ```

   (2) see README.MD in corresponding cookiecutter for additional info/steps

     
