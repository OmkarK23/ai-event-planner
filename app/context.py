"""
Shared app context: loads the trained model, label encoders, and historical
data once, and re-exports the canonical category lists from
generate_dataset.py so every page pulls dropdown options from the same
source the model was actually trained on, instead of separately hardcoded
lists that can drift out of sync.
"""

import os
import sys

import joblib
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(SRC_DIR)

from generate_dataset import EVENT_TYPES, DAYS, TIMES, LOCATIONS, PROMO_CHANNELS  # noqa: E402
from database import create_table  # noqa: E402

MODEL_PATH = os.path.join(CURRENT_DIR, "..", "models", "attendance_model.pkl")
ENCODERS_PATH = os.path.join(CURRENT_DIR, "..", "models", "label_encoders.pkl")
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "event_data.csv")

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODERS_PATH)  # {'event','day','time','location','promo': LabelEncoder}
df = pd.read_csv(DATA_PATH)

create_table()
