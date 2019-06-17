#!./venv/bin/python3.6
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import logging
logging.basicConfig(stream=sys.stderr)

from start_service import app as application
