#!/bin/bash

# Load configuration variables from config.sh
source ./config.sh

# Function to build the Docker image
build_image() {
  if [ -z "$DOCKER_FILE" ]; then
    echo "Error: Dockerfile path not provided. Please specify the Dockerfile path."
    exit 1
  fi

  echo "Building Docker image $IMAGE_NAME:$IMAGE_TAG with Dockerfile $DOCKER_FILE..."
  docker build -f "$DOCKER_FILE" -t "$IMAGE_NAME:$IMAGE_TAG" "$DIR"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to build the Docker image."
    exit 1
  fi

  echo "Docker image $IMAGE_NAME:$IMAGE_TAG built successfully."
}

# Function to start the Docker container
start_container() {
  # Check if the service container is running
  if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing the existing container..."
    docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
  fi

  # Check if the service container exists but is not running
  if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
    echo "Removing the existing stopped container..."
    docker rm $CONTAINER_NAME
  fi

  # Run the service container
  echo "Starting container $CONTAINER_NAME..."
  docker run -it -p 9002:9000 --restart always \
    --name $CONTAINER_NAME -v "$DIR":/app \
    --env-file .env "$IMAGE_NAME:$IMAGE_TAG" bash
  if [ $? -ne 0 ]; then
    echo "Error: Failed to start the container."
    exit 1
  fi

  echo "Container $CONTAINER_NAME started successfully."
}

# Check arguments
case $1 in
  build)
    if [ -z "$2" ]; then
      echo "Error: Dockerfile path is required for the build command."
      exit 1
    fi
    DOCKER_FILE=$2
    build_image
    ;;
  start)
    start_container
    ;;
  *)
    echo "Usage:"
    echo "./entrypoint.sh build <Dockerfile>  - Build the Docker image"
    echo "./entrypoint.sh start              - Start the Docker container"
    exit 1
    ;;
esac
