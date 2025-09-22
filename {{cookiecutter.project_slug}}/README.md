# {{ cookiecutter.project_name }}

## Run with uv

### Install uv

**for windows (powershell)**
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
- after running the above command add uv to path as instructed in powershell

**for linux/mac**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**install with pip**
```sh
pip install uv
```

---

### Run

```sh
uv run -m --no-dev uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Installation without uv

```sh
python -m venv .venv
# for windows
.venv\Scripts\activate
# for linux
# source .venv/bin/activate
pip install -r requirements.txt
```
---

{%- if cookiecutter.use_docker == "yes" -%}

## Build with Docker

Add non source code files and folder to `.dockerignore`


```sh
docker build -t {{cookiecutter.project_slug}}:1.0 .
```

## Run

**with docker-compose**
```sh
docker-compose up -d
```
**manually**
```sh
docker run -p 8000:8000 {{cookiecutter.project_slug}}:1.0
```
{% endif %}