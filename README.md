# Sheets Cleanup Tool

A Streamlit application for cleaning and managing article submission data from Google Sheets.

## Features
- Upload CSV files from Google Sheets
- Filter articles based on submission status
- Keep 'New Article' and 'Needs Review' entries
- Remove completed submissions
- Download cleaned data as CSV

## How to Use
1. Download your Google Sheet as a CSV file
2. Upload the CSV file to the application
3. Click 'Clean Data' to process the file
4. Download the cleaned CSV file

## Setup for Local Development
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run sheets_cleanup.py
   ```

## Deployment
This application is deployed on Streamlit Cloud and can be accessed at [Streamlit App URL].

## Requirements
- Python 3.7+
- See requirements.txt for all dependencies 