# A&E Attendances: End-to-End ETL + Dashboard Project

## Overview

This was my first project where I learned about API's and ETL concepts. I created a python script to extract data relating to A&E activity in St John's Hospital, transform and load the data into PostgreSQL. The database is connected to Power BI to visualise it.

## Workflow
1. Python script extracts data from the NHS Scotland's open API
2. Transforms data (cleaning, column renaming)
3. Loads new rows into PostgreSQL
4. Power BI dashboard is built on top of the database, showing key metrics from latest week and trends over time
5. Scheduled via Windows Task Scheduler to run every Wednesday morning
