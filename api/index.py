import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import app

# Vercel Python runtime will use the Flask app object from this module.
# Ensure this file stays in the api/ folder and vercel.json routes all traffic here.
