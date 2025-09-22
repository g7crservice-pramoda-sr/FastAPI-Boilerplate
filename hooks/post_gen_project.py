import os
import shutil
from pathlib import Path

# Path to the generated project directory
project_dir = Path.cwd()

use_docker = "{{ cookiecutter.use_docker }}".lower()

if use_docker != "yes":
    for fname in ["Dockerfile", "docker-compose.yml", ".dockerignore"]:
        fpath = project_dir / fname
        if fpath.exists():
            if fpath.is_file():
                fpath.unlink()         # delete file
            elif fpath.is_dir():
                shutil.rmtree(fpath)    # delete folder if needed
