setup:
	@echo "Setting up environment"
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	mkdir -p dags src/ingestion src/transformation src/validation src/utils
	mkdir -p data/raw data/cleaned docker/airflow notebooks sql tests
	touch Dockerfile docker-compose.yml requirements.txt README.md .env

run-airflow:
	@echo "Starting Airflow with Docker"
	docker-compose up airflow-init
	docker-compose up

stop:
	@echo "Stopping Docker containers"
	docker-compose down

clean:
	@echo "Cleaning environment"
	rm -rf venv __pycache__ .pytest_cache .env
