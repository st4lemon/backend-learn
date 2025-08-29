# backend-learn
## Project Goals
- First backend application: Learn how to set up APIs with FastAPI, and how to manage a PostgreSQL database
- Utilize API endpoints and metadata in the database to train, manage, and store trained SKLearn models'
- TODO: Generate an API doc

### Tech Stack
- Backend only: FastAPI, PostgreSQL (with psycopg2 and asyncpg)

## Installation

- Python 3.12+
- PostgreSQL 17 and postgresql-contrib
- libpq-dev

Run `pip install -r requirements.txt` to install dependencies

## Running the app locally
- Start a Postgres service with `sudo systemctl start postgresql` on port 5432
- `source venv/bin/activate` to activate a Python virtual environment with dependencies installed
- `uvicorn backend.main:app --reload` to host the app locally on 127.0.0.1:8080

## Changelog
- 8/27/2025: Add GET model and POST predict endpoints + tester notebook. TODO: add unit testing for APIs
- 8/25/2025: Add verification to Upload endpoints to ensure a target column is included, add GET endpoints to view data. 
- 8/23/2025: Create Data upload endpoints to receive datasets
- 8/21/2025: Create Website upload endpoint to learn FastAPI
