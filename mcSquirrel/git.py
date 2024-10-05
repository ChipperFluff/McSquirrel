import os
import subprocess
from .logger import log, handle_error

def init_repo():
    try:
        if not os.path.exists('.git'):
            log("Initializing new git repository...")
            subprocess.run(['git', 'init'], check=True)
            log("Git repository initialized successfully.")
        else:
            log("Git repository already exists. Skipping initialization.")
    except Exception as e:
        handle_error(f"Failed to initialize git repository: {e}")

def commit_changes(msg: str):
    try:
        log("Preparing to commit changes...")
        init_repo()

        log("Adding changes to staging area...")
        subprocess.run(['git', 'add', '.'], check=True)

        log(f"Committing changes with message: '{msg}'")
        subprocess.run(['git', 'commit', '-m', msg], check=True)
        log("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        handle_error(f"Git command failed: {e}")
    except Exception as e:
        handle_error(f"Failed to commit changes: {e}")
