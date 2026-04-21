import os
import shutil
from pathlib import Path

# Path to the generated project directory
project_dir = Path.cwd()

use_docker = "{{ cookiecutter.use_docker }}".lower()
# Check if input starts with 'y' (e.g., 'y', 'yes')
is_docker = use_docker.startswith('y')

extract_to_current_folder = "{{ cookiecutter.extract_to_current_folder }}".lower()
is_extract = extract_to_current_folder.startswith('y')

# 1. Clean up Docker files if not needed
if not is_docker:
    for fname in ["Dockerfile", "docker-compose.yml", ".dockerignore"]:
        fpath = project_dir / fname
        if fpath.exists():
            if fpath.is_file():
                fpath.unlink()
            elif fpath.is_dir():
                shutil.rmtree(fpath)

# 2. Extract into current folder if requested
if is_extract:
    parent_dir = project_dir.parent
    
    for item in project_dir.iterdir():
        # Move items one by one to parent
        dest = parent_dir / item.name
        
        # If destination already exists, remove it first to avoid move errors
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        
        shutil.move(str(item), str(dest))
    
    # The current directory is now empty (except maybe for the hook script itself if it's here)
    # Since we can't easily delete the CWD on some OSes while executing, 
    # we'll exit and let the directory be, or try to delete it.
    # Typically, the folder remains empty and the user just uses the files in .
    # But we can try to remove it if possible.
    try:
        os.chdir(parent_dir)
        shutil.rmtree(project_dir)
    except Exception:
        # On Windows, the directory might be locked by the process that invoked the hook.
        # We try a background shell command to delete it after a short delay.
        if os.name == 'nt':
            # Use cmd /c with a delay to let the hook process exit and release handles
            cmd = f'start /b cmd /c "timeout /t 2 > nul && rd /s /q \"{project_dir}\""'
            os.system(cmd)
        else:
            # On Unix-like systems, we can try a similar background rm
            os.system(f'(sleep 2; rm -rf "{project_dir}") &')
