import os
import textwrap
from pathlib import Path
from typing import Optional


def test_for_colab() -> bool:
    """Return True if running in Google Colab; mounts Drive if present."""
    try:
        from google.colab import drive  # type: ignore
        print("Running in Google Colab environment. Mounting Google Drive...")
        drive.mount('/content/drive')
        return True
    except ImportError:
        return False


def run_colab_setup_bash(project_name: str, install: bool = True) -> None:
    """Execute the original one-line Colab bash setup as a single call.

    Runs the following in a Bash cell (via IPython):
      - mkdir -p ~/.ssh/
      - cp id_rsa, id_rsa.pub, known_hosts from Drive
      - chmod 600 on the private key
      - pwd
      - git clone git@github.com:essans/{PROJECT_NAME}.git
      - cd into {PROJECT_NAME}
    """
    
    script = textwrap.dedent(f"""
        mkdir -p ~/.ssh/
        cp /content/drive/MyDrive/colabSSH/id_rsa ~/.ssh/id_rsa
        cp /content/drive/MyDrive/colabSSH/id_rsa.pub ~/.ssh/id_rsa.pub
        cp /content/drive/MyDrive/colabSSH/known_hosts ~/.ssh/known_hosts
        chmod 600 ~/.ssh/id_rsa
        pwd
        git clone git@github.com:essans/{project_name}.git || echo 'clone skipped (directory likely exists)'
    """).strip()

    try:
        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        if ip is None:
            raise RuntimeError("IPython not available; cannot run bash cell.")
        ip.run_cell_magic('bash', '', script)
        ip.run_line_magic('cd', project_name)

        if install:
            print('--> installing required libraries')
            # Use IPython %pip magic so installs apply to the current kernel
            ip.run_line_magic('pip', 'install -e . --no-deps')
    except Exception as e:
        print(f"Warning: Could not run bash setup via IPython: {e}")
        print("You can run the commands manually in a notebook cell.")


def colab_upload_data_and_setup_path(project_name: str, data_dir: str = "/content/drive/MyDrive/data") -> None:
    """
    In Colab, open a file upload dialog, move uploaded files into the given
    Google Drive folder, then switch back to the cloned repo and add its `src`
    to `sys.path`.

    Mirrors the notebook snippet:
      - from google.colab import files
      - os.chdir('/content/drive/MyDrive/data')
      - uploaded = files.upload()
      - print per-file summary
      - os.chdir(f'/content/{project_name}')
      - sys.path.append(f"{Path().resolve()}/src")
    """

    import importlib
    try:
        files_mod = importlib.import_module('google.colab.files')
    except ModuleNotFoundError:
        print("Not running in Google Colab; skipping upload and path setup.")
        return

    import sys
    from pathlib import Path

    try:
        os.chdir(data_dir)
    except Exception as e:
        print(f"Warning: could not change to data_dir {data_dir}: {e}")

    uploaded = files_mod.upload()
    for fn in uploaded.keys():
        print('User uploaded file "{name}" with length {length} bytes'.format(
            name=fn, length=len(uploaded[fn])))

    repo_dir = f"/content/{project_name}"
    try:
        os.chdir(repo_dir)
    except Exception as e:
        print(f"Warning: could not change directory to {repo_dir}: {e}")

    sys.path.append(f"{str(Path().resolve())}/src")


def colab_set_hf_token() -> None:
    """
    Retrieve HF_TOKEN from Colab secrets and set it as an environment variable.

    In Colab, you can store secrets via the Secrets tab and access them via
    `google.colab.userdata.get('hf_api_key')`.

    This function:
      - Attempts to import google.colab.userdata
      - Retrieves 'hf_api_key' from Colab secrets
      - Sets os.environ['HF_TOKEN'] if found
      - Prints a warning if not found or on error
    """
    import importlib

    try:
        userdata_mod = importlib.import_module('google.colab.userdata')
    except ModuleNotFoundError:
        # Not running in Colab; skip silently
        return

    try:
        api_key_value = userdata_mod.get('hf_api_key')
        if api_key_value is None:
            print("Warning: 'hf_api_key' not found in Colab secrets.")
        else:
            os.environ['HF_TOKEN'] = api_key_value
            print("HF_TOKEN successfully set from Colab secrets.")

    except Exception as e:
        print(f"An unexpected error occurred while retrieving HF_TOKEN: {e}")