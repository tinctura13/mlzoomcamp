# Build the Docker container
build:
	@echo "Building Docker container..."
	docker build --no-cache -t capstone01-tinctura .

# Run the Docker container
run:
	@echo "Running Docker container on port 8080..."
	docker run -p 8080:8080 capstone01-tinctura

# Test service availability
ping:
	curl http://0.0.0.0:8080/health