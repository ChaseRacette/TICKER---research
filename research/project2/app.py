"""Compatibility entry point for the deployed Streamlit app.

The canonical Project 2 source lives in the top-level ``Project 2`` folder.
This small bridge preserves the existing Streamlit Community Cloud entry-point
path while the deployment configuration catches up with the clearer layout.
"""
from pathlib import Path
import runpy

CANONICAL_APP = Path(__file__).resolve().parents[2] / "Project 2" / "app.py"
runpy.run_path(str(CANONICAL_APP), run_name="__main__")
