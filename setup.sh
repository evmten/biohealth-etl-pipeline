#!/bin/bash

echo "Setting up your data pipeline project environment..."

python3 -m venv venv
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found."
fi

mkdir -p dags
mkdir -p src/ingestion src/transformation src/validation
mkdir -p data/raw data/cleaned
mkdir -p airflow
# mkdir -p notebooks
mkdir -p sql
mkdir -p tests

touch Dockerfile docker-compose.yml requirements.txt README.md .env

echo "Set up is done!"
