# Setup Instructions
## System Setup (Ubuntu 24.04)
Run the following commands to prepare your system:
```shell
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install compilers and development tools
sudo apt install -y build-essential

# Add Python 3.12 (deadsnakes PPA)
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12 and tools
sudo apt install -y python3.12 python3.12-dev python3.12-venv python3.12-distutils

# Install Uvicorn for running the API
sudo apt install -y uvicorn

# Upgrade pip and setup tools
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --upgrade pip
```

# Virtual Environment Setup
## Create and activate virtual environment
```shell
python3.12 -m venv venv
source venv/bin/activate

# Install build tools
pip install --upgrade cython wheel

# Install project dependencies
pip install -r prod-requirements.txt
```

## Initialize the Local Database
With the virtual environment activated:
```shell
python src/create_db.py
```
# Run the API
```shell
python src/main.py
```

## Visit the interactive docs at:
📍 http://localhost:8000/docs (Swagger UI)

# Run with Docker
```shell
docker build -t api .
docker run -p 8000:8000 api
```

## Access Logs Inside the Container
```shell
sudo docker exec -it <CONTAINER_ID> cat logs/app.log
```

## Data Input
To test company classification, use the sample file:
files/process_companies.json

Each entry contains a dynamic features field stored as JSON — designed to support unstructured and unpredictable input data.

## Logging
A logs/ folder is created on the first run.
All requests, responses, and errors are logged for traceability.

## Testing
Unit tests cover common and edge cases for each endpoint.

A mock database is used to simulate various scenarios.

## Run Tests
With the virtual environment activated and dev-requirements.txt installed:
```shell
pytest tests/
```

# ML Logic – V2
This version uses TF-IDF to assess the importance of words in a company description. Instead of checking for predefined keywords, it outputs a probability score indicating whether a company is SaaS.

## Model: Dummy LogisticRegression

## Flexible: Swappable/tunable models

## Learn more: See ml_dummy_models.py

