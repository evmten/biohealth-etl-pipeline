#!/bin/bash

echo "🔧 Setting up your data pipeline project environment..."

python3 -m venv venv
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📚 Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found. Skipping install."
fi

mkdir -p dags
mkdir -p src/ingestion src/transformation src/validation src/utils
mkdir -p data/raw data/cleaned
mkdir -p docker/airflow
mkdir -p notebooks
mkdir -p sql
mkdir -p tests

touch Dockerfile docker-compose.yml requirements.txt README.md .env

echo "✅ All set up!"
