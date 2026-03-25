# WGU Data Analytics Degree Tracker
A Python-based CLI application designed to track academic progress, manage course data using SQLite, and perform performance analytics.

## Project Overview
This tool was developed to move beyond a simple spreadsheet and create a robust data pipeline for tracking degree progress. It features a custom **Data Backfill** algorithm that handles missing historical data by applying academic term logic to calculate completion velocity.

## Tech Stack
* **Language:** Python 3.x
* **Database:** SQLite3
* **Libraries:** `csv`, `datetime`, `os`

## Key Features
* **Predictive Graduation Modeling:** Uses historical velocity data (Avg Days per Course) to forecast a specific graduation month and year.
* **Database Migrations:** Automated schema updates to add new tracking columns without losing data.
* **Performance Analytics:** Calculates average days to complete a course to estimate a graduation date.
* **Smart Backfill:** Uses logic-based imputation to fill missing `date_started` values based on WGU term starts (Aug 1st / Feb 1st).
* **CSV Export:** Generates professional reports for external analysis in Excel or Tableau.

## Database Schema
The project uses an SQLite database with the following structure:
* `course_id`: Primary Key (e.g., D493)
* `course_name`: Title of the course
* `status`: Current state (Completed, In Progress, Not Started)
* `date_started`: The start date of the attempt
* `date_finished`: The date of final assessment completion

## Analytics Logic
The "Velocity" is calculated using the following formula:
$$\text{Avg Pace} = \frac{\sum (\text{Date Finished} - \text{Date Started})}{\text{Total Courses Completed}}$$

## Lessons Learned
* **Schema Evolution:** Implemented `ALTER TABLE` within a `try/except` block to ensure the database can grow without losing existing student data (Idempotency).
* **Data Persistence:** Transitioned from a volatile "re-populate" script to a persistent SQLite storage model to ensure progress isn't overwritten on restart.
* **Separation of Concerns:** Refactored the CLI menu into `main.py` while keeping database logic in a separate module for better maintainability.

## Roadmap
* **Predictive Graduation Modeling:** Use current velocity (30.1 days) to forecast a specific graduation month.
* **Data Visualization:** Integration with Matplotlib to generate a "Burndown Chart" of remaining credits.

## How to Use
1. Run the script: `main.py`
2. Select **Option 4** (Run Backfill) to align historical data.
3. Use **Option 2** to update current course status.
4. Select **Option 3** to see current completion percentage and your AI-projected graduation date.
5. Export your data to CSV using **Option 5** for external reporting.