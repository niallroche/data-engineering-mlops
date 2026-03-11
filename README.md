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
# Project Brief: Data Engineering Team Activity

## Overview
Your task is to develop a simple end-to-end system that:
- Trains a basic logistic regression model (using scikit-learn)
- Serves the model via a Flask API
- Logs API calls and predictions in a PostgreSQL database
- Containerizes the components with Docker
- Deploys the pipeline to a cloud platform (using free credits)
- Develops API documentation (and optionally a Postman script) so other groups can use your API

## Repository and Collaboration

1. **Forking the Base Repository**
   - One group should fork the provided base repository. This repo will serve as your project starting point.
   - The main group member (team lead) should then add the other team members as collaborators to the group repository.

2. **Cloning and Contributing**
   - Each team member should clone the main group repository to their local machines.
   - All initial contributions should be made directly into this single repository.
   - Once you become comfortable with the workflow, experiment by having individual team members fork the group repository into their own personal repos.
   - Practice making pull requests (PRs) from these forks. Each PR must be reviewed and approved by at least two team members before merging into the main repository.

## Team Roles
Assign roles based on the following suggestions:
- **Model Developer:** Implements and trains the logistic regression model.
- **API Developer:** Develops the Flask API (including a static HTML form and unit tests).
- **Database Engineer:** Sets up and integrates PostgreSQL for logging.
- **DevOps/CI-CD Engineer:** Handles Docker containerization, GitHub Actions for deployment, and ensures proper cloud deployment.
- **Documentation Specialist (optional):** Develops API documentation and a Postman script to help other groups use your API.

## Workflow
- **Initial Development:** Work on the main repository by committing and pushing your changes.
- **Experiment with Forking:** Once comfortable, try forking the repo, making changes, and submitting pull requests. This helps simulate a real-world multi-repository workflow.
- **Code Review:** Every pull request should be reviewed by at least two team members. Use the review process to discuss improvements and ensure code quality.

## Cloud Deployment
- **Platform Choice:** Choose a cloud platform for deployment (GCP, AWS, or any platform offering free credits).
- **Free Credits:** Use the free credits available, but be cautious of cost overruns.
- **Security:** Make sure to follow best practices regarding credentials and resource permissions.
- **Deployment Automation:** Use GitHub Actions (or another CI/CD tool) to automate the deployment process.

## API Documentation and Postman Script
- **Documentation:** Develop comprehensive API documentation that explains:
  - Available endpoints (e.g., `/predict`)
  - Expected input data and output format
  - How to authenticate (if applicable)
  - Example requests and responses
- **Postman Script:** Optionally, create a Postman collection that contains:
  - A script for testing the API endpoints.
  - Pre-configured requests so other groups can easily import the collection and test your API.

## Final Deliverables
- A working system deployed on the cloud platform.
- A fully documented API (with a README and additional documentation if needed).
- A Postman collection file (optional) for easy API testing.
- A summary of your workflow, including how you used forks, pull requests, and reviews to merge changes.

---

**Remember:**  
- The main repository is your base. Use forks and PRs to experiment with collaborative workflows.
- Ensure that you keep track of costs and follow best security practices during cloud deployment.
- Good documentation is key—make it easy for other groups to understand and use your API.

Good luck, and happy coding!

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

Note, the use_database environment variable is set to false, so the database will not be created and the logs will not be saved to the database

to run the server with the database enabled, run the following command
```bash
# find the container id running the api
docker ps
# stop the container
docker stop <container_id>
# run the container again with the database enabled
docker run -p 5000:5000 -e DB_ENABLED=true <container_id>
# or just change the value of the use_database environment variable to true in the docker-compose.yml file    
```

2. Manual Setup:
```bash
# Connect to PostgreSQL in the container
# if using docker desktop then connect to a terminal for the running container

# find the container id running the api
docker ps
docker exec -it <container_id> psql -U postgres


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

---

### Deploying to Google Cloud Run (Web Console)

This section explains how to deploy the ML model API to Google Cloud Run using the Google Cloud Web Console.

#### Part 1 — Create a Google Cloud Account

Open the Google Cloud Console: https://console.cloud.google.com

Sign in using a Google account. If this is your first time using Google Cloud you will be prompted to start the free trial and enable billing. The free trial provides credits which are sufficient for this lab.

#### Part 2 — Create a New Project

Projects are the top-level container for all Google Cloud resources.

1. Click the **Project Selector** in the top navigation bar
2. Click **New Project**

Enter:
- **Project name:** `mlops-lab-group1`
- **Organization:** leave blank
- **Location:** No organization

Click **Create**. After creation, make sure your new project is selected in the top menu.

#### Part 3 — Enable Required APIs

Navigate to **APIs & Services → Library** and enable the following APIs:

| API | Purpose |
|-----|---------|
| **Cloud Run API** | Runs the containerised service |
| **Artifact Registry API** | Stores container images |
| **Cloud Build API** | Builds container images from source |
| **Secret Manager API** *(optional)* | Secure storage for credentials/API keys |
| **Vertex AI API** *(optional)* | Advanced ML model hosting |

#### Part 4 — Create a Service Account

Navigate to **IAM & Admin → Service Accounts** and click **Create Service Account**.

Enter:
- **Name:** `mlops-lab-sa`
- **Description:** `Service account for MLOps lab deployment`

Click **Create** and assign the following roles:
- Cloud Run Admin
- Artifact Registry Writer
- Cloud Build Editor
- Service Account User

Click **Done**.

#### Part 5 — Create an Artifact Registry

Navigate to **Artifact Registry → Repositories** and click **Create Repository**.

Fill in:
- **Name:** `ml-models`
- **Format:** Docker
- **Mode:** Standard
- **Region:** `europe-west2` (London)

Click **Create**. The registry is now ready to store container images built by Cloud Build.

#### Part 6 — Deploy the Service to Cloud Run

Navigate to **Cloud Run → Create Service** and choose **Deploy from source repository**.

If GitHub is not yet connected, click **Set up Cloud Build** and follow the prompts to connect your GitHub account.

Once connected:
- Select your repository (e.g. `data-engineering-mlops`)
- Choose the branch: `main`
- Select the folder containing the API (e.g. `api/`)

#### Part 7 — Configure the Cloud Run Service

| Setting | Value |
|---------|-------|
| **Service name** | `ensemble-gateway` |
| **Region** | `europe-west2` |
| **Authentication** | Allow unauthenticated |
| **Port** | `8080` |
| **Min instances** | `0` |
| **Max instances** | `5` |
| **CPU** | `1` |
| **Memory** | `512 MB` |

Click **Create**. Cloud Run will build the container image, push it to Artifact Registry, and deploy a new service revision. Deployment usually takes 1–2 minutes.

#### Part 8 — Retrieve the Public API URL

After deployment finishes, Cloud Run displays a **Service URL**, for example:

```
https://ensemble-gateway-abc123-ew2.a.run.app
```

If you are using FastAPI, the Swagger docs are available at:

```
https://SERVICE_URL/docs
```

#### Part 9 — Test the API Endpoint

```bash
export SERVICE_URL=https://ensemble-gateway-abc123-ew2.a.run.app

curl -X POST "$SERVICE_URL/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Expected response:

```json
{
  "prediction": 1,
  "confidence": 0.83
}
```

#### Troubleshooting

**Container failed to start**

Ensure the application listens on `0.0.0.0:8080`. Cloud Run sets the `PORT` environment variable automatically:

```python
import os
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
```

**Model file not found**

If you see `FileNotFoundError: model/logistic_model.pkl`, ensure the model file exists inside the container image. Your project structure should look like:

```
repo/
├── api/
│   └── app.py
├── model/
│   └── logistic_model.pkl
└── Dockerfile
```

And the Dockerfile must copy the model directory:

```dockerfile
COPY . /app
```

**Verify application startup locally**

Before deploying, test on the Cloud Run port:

```bash
PORT=8080 python api/app.py
# or
PORT=8080 uvicorn api.app:app --host 0.0.0.0 --port 8080
```

**scikit-learn version mismatch**

If you see `'LogisticRegression' object has no attribute 'multi_class'`, the model was pickled with a different scikit-learn version than the one in `requirements.txt`. Retrain the model after installing the pinned version:

```bash
pip install scikit-learn==1.6.1
python model/train_model.py
```

Commit the updated `logistic_model.pkl` and redeploy.

---

## How to Deploy to AWS

### Prerequisites
- An AWS account.
- The AWS CLI installed on your machine.
- A service account key for the AWS project.