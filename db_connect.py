# db_connect.py
# Provides a reusable MySQL connection function for the PhonePe Insights project.

import mysql.connector
import streamlit as st

def get_connection():
    try:
        # Cloud deployment — use Streamlit secrets
        cfg = st.secrets["mysql"]
        return mysql.connector.connect(
            host=cfg["host"], port=cfg["port"],
            user=cfg["user"], password=cfg["password"],
            database=cfg["database"], ssl_disabled=False
        )
    except Exception:
        # Local fallback
        return mysql.connector.connect(
            host="localhost", user="root",
            password="your_local_password",  # <-- your local MySQL password
            database="phonepe_pulse"
        )