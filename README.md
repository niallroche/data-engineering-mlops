# Data Engineering Team Activity

This project is a simple end-to-end system built for Data Engineering students. The project demonstrates how to:

- Train a basic logistic regression model using scikit-learn.
- Serve the model via a Flask REST API.
- Log API request parameters and model predictions into a PostgreSQL database.
- Containerize the application using Docker and Docker Compose.
- Provide a static HTML form to test the API.
- Run a simple unit test for the API.
- (Optional) Deploy the entire pipeline to Google Cloud Platform (GCP) using GitHub Actions.

## Project Structure

The project is organized into the following key directories and files:
```
├── model
│   └── train_model.py         # Train and save the logistic regression model
│   └── test_model.py          # Unit tests for the model
│   └── logistic_model.pkl     # trained logistic regression model (needs to be trained first)
├── api
│   ├── app.py                 # Flask API to serve predictions and log data to PostgreSQL
│   └── test_app.py            # Unit tests for the API
├── db/
│   └── init.sql               # SQL script to create the prediction_logs table
├── static
│   └── index.html             # Static HTML form to call the API
├── Dockerfile                 # Dockerfile for containerizing the Flask API
├── docker-compose.yml         # Docker Compose configuration (starts API and PostgreSQL containers)
├── requirements.txt           # Python dependencies
└── .github
│    └── workflows
│       └── deploy.yml                 # GitHub Actions workflows for deploying to cloud 
```

## Setup Instructions
clone this repository

### Prerequisites
Docker installed on your machine and running

## How to Run Locally
### Prerequisites
- Git installed on your machine
- Docker installed on your machine and running
- Python 3.9+ installed (if running locally without Docker)

1. Clone the repository:

```bash
git clone https://github.com/niallroche/data-engineering-mlops.git
```

2. Navigate to the project directory:

```bash
cd data-engineering-mlops
```

### Setup Dependencies
- If running without Docker, install the required Python packages:
create a virtual environment and activate it

```bash
python -m venv de-venv
source de-venv/bin/activate
```

install the required Python packages:

```bash
pip install -r requirements.txt
```

### 1. Train the Model
- Navigate to the `model` folder.
- Run the training script to build the logistic regression model and save it to `model/logistic_model.pkl`.

```bash
cd model
python train_model.py
```

- Run Unit Tests
- Navigate to the root directory of the project.
- Run the following command to run the unit tests for the model.

```bash
cd ..
python -m unittest model/test_model.py
```

### 2. Build the Docker image:
- Navigate to the root directory of the project.
- Run the following command to build the Docker image. (Note that this command might require admin rights such as sudo)

```bash
docker-compose build
```

### 3. Start the API
- Navigate to the root directory of the project.
- Run the following command to start the API and optionally the PostgreSQL containers.

```bash
docker-compose up -d
```
- to run the server locally outside of docker run the following in a dedicated terminal window
```bash
python3 api/app.py
```

### 4. Run Unit Test
- Navigate to the root directory of the project.
- Run the following command to run the unit tests for the API.

```bash
python -m unittest api/test_app.py
```

### 5. Test the API
- set the USE_DATABASE environment variable to false 

```bash
USE_DATABASE=false
```
- Open your web browser and navigate to `http://localhost:5000`.
- Fill in the form with the required fields and click the "Predict" button to see the model's prediction.

### 6. Test the API using curl
- Navigate to the root directory of the project.
- Run the following command to test the API using curl.

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### 7. Shutdown the containers
- Navigate to the root directory of the project.
- Run the following command to shutdown the containers.

```bash
docker-compose down
```

## Database Setup

### Schema
The application uses PostgreSQL to store prediction logs with the following schema:

```sql
CREATE TABLE prediction_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    input_features JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    model_version TEXT DEFAULT '1.0',
    confidence FLOAT,
    processing_time FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### Key Fields:
- `id`: Unique identifier for each prediction
- `timestamp`: When the prediction was made
- `input_features`: JSON object containing the input parameters
- `prediction`: The model's output prediction
- `model_version`: Version of the model used
- `confidence`: Confidence score of the prediction (if available)
- `processing_time`: Time taken to process the request
- `created_at`: Record creation timestamp

### Setup Instructions

1. Using Docker Compose (Recommended):
```bash
docker-compose up -d
```
This will automatically:
- Create the PostgreSQL database
- Initialize the schema
- Set up the required users and permissions

2. Manual Setup:
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE flask_logs;

# Connect to the new database
\c flask_logs

# Run the schema initialization script
\i db/init.sql
```

2. Connect to PostgreSQL in Docker:
```bash
# find the container id running PostgreSQL
docker ps

# connect to the container
docker exec -it <container_id>

# connect to the database
psql -U postgres -d flask_logs

# list the database tables
\dt

# select recordfrom the table
select * from prediction_logs;

# exit the database
\q

```

if the database needs to be created first, execute the following command when logged in to the container
```bash
psql -U postgres -d flask_logs -f /docker-entrypoint-initdb.d/init.sql
```

### Environment Variables
Configure the following environment variables for database connection:
```bash
USE_DATABASE=true
POSTGRES_DB=flask_logs
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Accessing Logs
Query recent predictions:
```sql
SELECT * FROM recent_predictions;
```

Monitor database size:
```sql
SELECT pg_size_pretty(pg_database_size('flask_logs'));
```

## Running the Application
...


publish the image to a container registry 
- (to a GCP registry)
```bash
docker tag data-engineering-mlops:latest gcr.io/data-engineering-mlops/data-engineering-mlops:latest
docker push gcr.io/data-engineering-mlops/data-engineering-mlops:latest
```
- (to an AWS registry) change the tag to your own aws account id
```bash
docker tag data-engineering-mlops:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/data-engineering-mlops:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/data-engineering-mlops:latest
```

- to docker hub
```bash
docker tag data-engineering-mlops:latest niallroche/data-engineering-mlops:latest
docker push niallroche/data-engineering-mlops:latest
```

## How to Deploy to Cloud Platform

### Prerequisites
- A Google Cloud Platform (GCP) account.
- The Google Cloud SDK installed on your machine.
- A GCP project.
- A service account key for the GCP project.


## How to Deploy to AWS

### Prerequisites
- An AWS account.
- The AWS CLI installed on your machine.
- A service account key for the AWS project.