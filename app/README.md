## Running the Application

To run the application (*go to **app** dir first*) with Docker:

```bash
# Build the Docker image
docker build -t car-insurance-premium-simulator .

# Run the Docker container
docker run -p 8000:8000 -d car-insurance-premium-simulator

# Run tests
docker exec <DOCKER_CONTAINER_ID> pytest
```

You can then access the API at `http://localhost:8000/api/quote`.