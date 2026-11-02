"""Lets scripts run without `pip install -e .` by putting src/ on sys.path."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
