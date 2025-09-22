# FastAPI Boilerplate

Boilerplate code for FastAPI app

## Branches

- master
    - contains the bare minimum required to start the project
- docker
    - contains a boilerplate docker config including - `Dockerfile`, `.dockerignore` & `docker-compose.yml` 
- cookicutter
    - cookiecutter cli based initialization tool, highly customizable with cmd line parameters to setup everything required form one command.

## Master and Docker branch initialization

Just clone the respective branches using the below command and remove the .git folder.

```sh
git clone --branch master --single-branch https://github.com/g7crservice-pramoda-sr/FastAPI-Boilerplate.git ./<project_name>
```

Delete the `.git` folder to work on a fresh repo

## Cookiecutter branch initialization

Install cookiecutter

```sh
pip install cookiecutter
```

```sh
cookiecutter https://github.com/g7crservice-pramoda-sr/FastAPI-Boilerplate --checkout cookiecutter
```