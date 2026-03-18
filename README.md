# COMP3011 2026 Q1 Gaming Laptops Market API

## Project Overview
This project is an individual Web Services API developed for the COMP3011 module. It provides a RESTful API and a web application to query and manage market data for gaming laptops in Q1 2026. The API is built using Python and FastAPI, with data persistently stored in a local SQLite database. It supports full CRUD (Create, Read, Update, Delete) operations and 3 advanced analysis operations.

## Technology Stack
* **Framework:** FastAPI
* **Database:** SQLite3
* **Data Processing:** Pandas (for initial CSV to SQLite migration)
* **Server:** Uvicorn
* **Frontend:** HTML5 & Vanilla JavaScript + Tailwind CSS + Chart.js
* **Deployment:** Currently deploying on Render's free tier (Available at: https://comp3011-gaming-laptops-api-2026.onrender.com/)
* **Live API Documentation:** Currently deploying on Render's free tier (Available at: https://comp3011-gaming-laptops-api-2026.onrender.com/docs)

## Deliverables & API Documentation
As per the coursework requirements, the generated API documentation is provided as a PDF file. 
* **API Documentation:** [Link to PDF file](./API_DOC.pdf)

## Setup and Installation Instructions
Please follow these steps to run the API locally on your machine or within a GitHub Codespaces environment:

### Clone the repository
```bash
git clone <your-github-repo-url>
cd <your-repo-name>
```

## Set up the virtual environment
It is highly recommended to use a virtual environment to avoid dependency conflicts.
```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Initialize the Database
Before running the API, you must initialize the SQLite database using the provided dataset (gaming_laptops_2026_q1.csv). Run the following script:
```bash
python init_db.py
```

This will create a laptops.db file in the root directory containing the initial laptop records.

### Run the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be hosted locally at http://127.0.0.1:8000. You can access the interactive Swagger UI documentation by navigating to http://127.0.0.1:8000/docs in your web browser.