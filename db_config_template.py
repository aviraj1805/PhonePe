# db_config_template.py
# Rename this file to db_connect.py and fill in your MySQL credentials.

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="phonepe_pulse"
    )