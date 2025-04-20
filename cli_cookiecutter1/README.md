### cli_cookiecutter1

Overview:
- Useful for simple scripts
- Tested in Mac OS

<br>

## Installation: 

### Option1 -clone from local repo <br>
   (1) clone template repo to local drive <br>
   (2) from location where new project is to be created:<br>
   ```
   cookiecutter /path/to/cookiecutter_local_repo/cli_cookiecutter1
   ```
   
<br>

### option2: create new project based on remote github cookiecutter:
   (1) from location where new project is to be created:<br>
   
   ```
   cookiecutter https://github.com/essans/templates.git --directory cli_cookiecutter1

   or

   cookiecutter git@github.com:essans/templates.git --directory cli_cookiecutter1
   ```

if testing from a specific branch then:
   ```
   cookiecutter git@github.com:essans/templates.git --directory cli_cookiecutter1 -c branchname
   ```


     

