# A&E Attendance Data Pipeline

## Overview
An end-to-end ETL pipeline that extracts weekly A&E attendance data for St John's Hospital from the NHS Scotland Open Data API, transforms and loads it into a PostgreSQL database, and visualises it in Power BI.

Built as a personal project to develop data engineering skills including API integration, database design and pipeline automation.

## Data Source
NHS Scotland Open Data — Weekly A&E Activity and Waiting Times
https://www.opendata.nhs.scot/dataset/weekly-accident-and-emergency-activity-and-waiting-times

## Pipeline Architecture

1. **Extract** — Python script queries the NHS Scotland Open Data API, filtering to St John's Hospital
2. **Transform** — Data is cleaned, column names standardised and irrelevant fields removed
3. **Load** — Incremental load appends only new records to PostgreSQL, preventing duplicates on each run
4. **Visualise** — Power BI dashboard connected directly to the database, showing weekly performance metrics and trends over time
5. **Orchestration** — Scheduled via Windows Task Scheduler to run automatically every Wednesday morning with a log file recording each run

## Technical Decisions
- **Incremental loading** — prevents duplicate entries and preserves historical data
- **Environment variables** — avoids hardcoding sensitive information in the code
- **Automated scheduling with logging** — pipeline runs unattended with a timestamped log file to monitor success and failure

## Technologies Used
- Python (requests, pandas, sqlalchemy)
- PostgreSQL
- Power BI
- Windows Task Scheduler
