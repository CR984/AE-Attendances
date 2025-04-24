#!/usr/bin/env python
# coding: utf-8

# # API Project

# https://www.opendata.nhs.scot/dataset/weekly-accident-and-emergency-activity-and-waiting-times/resource/a5f7ca94-c810-41b5-a7c9-25c18d43e5a4

# ### Import Libraries

# In[24]:


import requests # For sending the API request
import json
from sqlalchemy import create_engine  # For connecting to a PostgreSQL database (or other databases)
import os
import openpyxl  # For reading and writing Excel (.xlsx) files
import pandas as pd


# ### Make the API request

# In[4]:


# API URL
url = "https://www.opendata.nhs.scot/api/3/action/datastore_search"

# Parameters
params = {
    "resource_id": "a5f7ca94-c810-41b5-a7c9-25c18d43e5a4",
    "limit": 1300,
    "filters": json.dumps({"TreatmentLocation": "S308H"})
}

# Send the request
response = requests.get(url, params=params)


# ### Interpret the result

# In[5]:


if response.status_code == 200:
    print(f"Request was a success! Status code: {response.status_code}")
else:
    print(f"Error: {response.status_code}")


# ### Print the records

# In[6]:


if response.status_code == 200:
    data = response.json()
    records = data.get("result", {}).get("records", [])  # Extract the records


# ### Add records to a data frame

# In[7]:


import pandas as pd

# Convert records to a DataFrame
df = pd.DataFrame(records)

# Show the first few rows
df.tail()


# # Transformation

# In[8]:


df.columns = df.columns.str.lower()
df = df.drop(columns = ["country", "hbt"])
df.head()


# # Add data to the database

# ### Create connection to the database

# In[9]:


# Create a connection to the database
db_user = "postgres"
db_password = "Chilli55"
db_host = "localhost"
db_port = "5432"
db_name = "A&E Attendances"

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

with engine.connect() as conn:
    print("Connected to PostgreSQL successfully!")


# ### Load data into the database

# In[10]:


existing_ids = pd.read_sql("SELECT _id FROM a_and_e_attendances", con=engine)['_id']
new_data = df[~df['_id'].isin(existing_ids)]

if not new_data.empty:
    new_data.to_sql("a_and_e_attendances", con=engine, if_exists="append", index=False)
    print(f"{len(new_data)} row(s) have been added to the database.")
else:
    print("Data already present within table.")

print("All data processed successfully!")





