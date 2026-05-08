# db_connect.py
# Provides a reusable MySQL connection function for the PhonePe Insights project.

import pymysql
import streamlit as st

def get_connection():
    try:
        cfg = st.secrets["mysql"]
        return pymysql.connect(
            host=cfg["host"], port=cfg["port"],
            user=cfg["user"], password=cfg["password"],
            database=cfg["database"], ssl={"ssl_disabled": False}
        )
    except Exception:
        return pymysql.connect(
            host="localhost", user="root",
            password="your_local_password",
            database="phonepe_pulse"
        )
