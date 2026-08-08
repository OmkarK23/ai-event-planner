import os
import sys

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, SRC_DIR)

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
