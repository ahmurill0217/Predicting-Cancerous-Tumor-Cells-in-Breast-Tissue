import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

names = ["IT Associate", "Registered Nurse", "Physician"]
usernames = ["IT", "rnurse", "physician"]
passwords = ["abc123", "def456", "ghi789"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(r'C:\Users\Admin\Desktop\Capstone Project\generate_keys.py').parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)