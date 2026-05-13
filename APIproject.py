#!/usr/bin/env python
# coding: utf-8

"""
A&E Attendance Data Pipeline
Extracts weekly A&E data for St John's Hospital from the NHS Scotland Open Data API,
transforms it and loads new records into a PostgreSQL database.
Scheduled to run weekly via Windows Task Scheduler.
"""



# --- Imports ---

import requests
from sqlalchemy import create_engine
import json
import os
import pandas as pd



# --- Extract ---

# NHS Scotland Open Data API endpoint
url = "https://www.opendata.nhs.scot/api/3/action/datastore_search"

# API query parameters
params = {
    "resource_id": "a5f7ca94-c810-41b5-a7c9-25c18d43e5a4", # Weekly A&E attendance dataset
    "limit": 1300, # Set above expected weekly records to ensure full dataset is returned
    "filters": json.dumps({"TreatmentLocation": "S308H"}) # Filter to SJH
}

# Send GET request to API
response = requests.get(url, params=params)

# Check response status
if response.status_code == 200:
    print(f"Request was a success! Status code: {response.status_code}")
else:
    print(f"Error: {response.status_code}")

# Parse JSON response and extract records
if response.status_code == 200:
    data = response.json()
    records = data.get("result", {}).get("records", [])  




# --- Transform ---

# Convert records to a DataFrame for tansformation
df = pd.DataFrame(records)

# Standardise column names to lower case for consistency
df.columns = df.columns.str.lower()

# Drop columns that are not required
df = df.drop(columns = ["country", "hbt"])




# --- Load ---

# Configure database connection settings
db_user = "postgres"
db_password = os.environ.get("DB_PASSWORD") # Password stored as environment variable to avoid hardcoding credentials
db_host = "localhost"
db_port = "5432"
db_name = "A&E Attendances"

# Create database engine and test connection
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
with engine.connect() as conn:
    print("Connected to PostgreSQL successfully!")

# Incremental load - only append records not already contained within the database
# Check existing ID's within the database to prevent duplicate entries being loaded
existing_ids = pd.read_sql("SELECT _id FROM a_and_e_attendances", con=engine)['_id']
new_data = df[~df['_id'].isin(existing_ids)]

# Append new records if any exist, otherwise confirm data is up to date
if not new_data.empty:
    new_data.to_sql("a_and_e_attendances", con=engine, if_exists="append", index=False)
    print(f"{len(new_data)} row(s) have been added to the database.")
else:
    print("Data already present within table.")

print("All data processed successfully!")
