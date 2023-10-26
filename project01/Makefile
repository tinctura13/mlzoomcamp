install:
	@echo "Installing pipenv..."
	pip install pipenv
	@echo "Creating virtual environment with pipenv..."
	pipenv --python 3
	@echo "Installing dependencies from Pipfile.lock..."
	pipenv sync

# Run the Flask app locally
run-app:
	@echo "Running Flask app locally on port 9696..."
	pipenv run gunicorn app:app --bind 0.0.0.0:9696

# Build the Docker container
build-docker:
	@echo "Building Docker container..."
	docker build --no-cache -t mlzoomproject .

# Run the Docker container
run-docker:
	@echo "Running Docker container on port 9696..."
	docker run -p 9696:9696 mlzoomproject:latest

# Test service availability
ping:
	curl http://0.0.0.0:9696/ping

# Test service prediction
prediction:
	curl http://0.0.0.0:9696/predict -X POST -H "Content-Type: application/json" -d '{"flat": {"location": "Алматы", "floor": 10, "area": 70.0, "is_furnished": "частично", "rooms": 3}}'
