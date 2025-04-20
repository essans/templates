from pathlib import Path
import streamlit as st


def get_project_dir():
    path = Path().absolute()
    markers = ['data', 'src', 'notebooks', '.git', 'configs', 'scripts', 'README.md']
    
    while path != path.parent:
        if any((path / marker).exists() for marker in markers):
            return path
        path = path.parent
    return None