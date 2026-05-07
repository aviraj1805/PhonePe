import os
import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="18082006",  # <-- Change this to your MySQL password
    database="phonepe_pulse"
)
cursor = conn.cursor()

BASE = "E:/pulse/data"

def get_states(path):
    return os.listdir(path)

# 1. Aggregated Transaction
print("Loading aggregated_transaction...")
path = f"{BASE}/aggregated/transaction/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for item in data["data"]["transactionData"]:
                pi = item["paymentInstruments"][0]
                cursor.execute("INSERT INTO aggregated_transaction(state,year,quarter,transaction_type,transaction_count,transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, item["name"], pi["count"], pi["amount"]))
conn.commit()
print("aggregated_transaction DONE")

# 2. Aggregated User
print("Loading aggregated_user...")
path = f"{BASE}/aggregated/user/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            agg = data["data"]["aggregated"]
            devices = data["data"].get("usersByDevice") or []
            if devices:
                for d in devices:
                    cursor.execute("INSERT INTO aggregated_user(state,year,quarter,registered_users,app_opens,device_brand,device_count,device_percentage) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (state, int(year), quarter, agg["registeredUsers"], agg["appOpens"], d["brand"], d["count"], d["percentage"]))
            else:
                cursor.execute("INSERT INTO aggregated_user(state,year,quarter,registered_users,app_opens,device_brand,device_count,device_percentage) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, agg["registeredUsers"], agg["appOpens"], None, None, None))
conn.commit()
print("aggregated_user DONE")

# 3. Aggregated Insurance
print("Loading aggregated_insurance...")
path = f"{BASE}/aggregated/insurance/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for item in data["data"]["transactionData"]:
                pi = item["paymentInstruments"][0]
                cursor.execute("INSERT INTO aggregated_insurance(state,year,quarter,insurance_type,insurance_count,insurance_amount) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, item["name"], pi["count"], pi["amount"]))
conn.commit()
print("aggregated_insurance DONE")

# 4. Map Transaction
print("Loading map_transaction...")
path = f"{BASE}/map/transaction/hover/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for item in data["data"]["hoverDataList"]:
                m = item["metric"][0]
                cursor.execute("INSERT INTO map_transaction(state,year,quarter,district,transaction_count,transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, item["name"], m["count"], m["amount"]))
conn.commit()
print("map_transaction DONE")

# 5. Map User
print("Loading map_user...")
path = f"{BASE}/map/user/hover/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for district, values in data["data"]["hoverData"].items():
                cursor.execute("INSERT INTO map_user(state,year,quarter,district,registered_users,app_opens) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, district, values["registeredUsers"], values["appOpens"]))
conn.commit()
print("map_user DONE")

# 6. Map Insurance
print("Loading map_insurance...")
path = f"{BASE}/map/insurance/hover/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for item in data["data"]["hoverDataList"]:
                m = item["metric"][0]
                cursor.execute("INSERT INTO map_insurance(state,year,quarter,district,insurance_count,insurance_amount) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, item["name"], m["count"], m["amount"]))
conn.commit()
print("map_insurance DONE")

# 7. Top Transaction
print("Loading top_transaction...")
path = f"{BASE}/top/transaction/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for district in (data["data"]["districts"] or []):
                m = district["metric"]
                cursor.execute("INSERT INTO top_transaction(state,year,quarter,entity_type,entity_name,transaction_count,transaction_amount) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "district", district["entityName"], m["count"], m["amount"]))
            for pincode in (data["data"]["pincodes"] or []):
                m = pincode["metric"]
                cursor.execute("INSERT INTO top_transaction(state,year,quarter,entity_type,entity_name,transaction_count,transaction_amount) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "pincode", pincode["entityName"], m["count"], m["amount"]))
conn.commit()
print("top_transaction DONE")

# 8. Top User
print("Loading top_user...")
path = f"{BASE}/top/user/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for district in (data["data"]["districts"] or []):
                cursor.execute("INSERT INTO top_user(state,year,quarter,entity_type,entity_name,registered_users) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "district", district["name"], district["registeredUsers"]))
            for pincode in (data["data"]["pincodes"] or []):
                cursor.execute("INSERT INTO top_user(state,year,quarter,entity_type,entity_name,registered_users) VALUES(%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "pincode", pincode["name"], pincode["registeredUsers"]))
conn.commit()
print("top_user DONE")

# 9. Top Insurance
print("Loading top_insurance...")
path = f"{BASE}/top/insurance/country/india/state"
for state in get_states(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            quarter = int(file.replace(".json", ""))
            with open(f"{path}/{state}/{year}/{file}") as f:
                data = json.load(f)
            for district in (data["data"]["districts"] or []):
                m = district["metric"]
                cursor.execute("INSERT INTO top_insurance(state,year,quarter,entity_type,entity_name,insurance_count,insurance_amount) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "district", district["entityName"], m["count"], m["amount"]))
            for pincode in (data["data"]["pincodes"] or []):
                m = pincode["metric"]
                cursor.execute("INSERT INTO top_insurance(state,year,quarter,entity_type,entity_name,insurance_count,insurance_amount) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (state, int(year), quarter, "pincode", pincode["entityName"], m["count"], m["amount"]))
conn.commit()
print("top_insurance DONE")

cursor.close()
conn.close()
print("\nAll 9 tables loaded successfully!")