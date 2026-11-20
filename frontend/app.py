"""
Frontend entry point redirecting to silvershield_frontend.py
"""
import runpy
from pathlib import Path

root_frontend = Path(__file__).parent.parent / "silvershield_frontend.py"
runpy.run_path(str(root_frontend), run_name="__main__")
