# Use the official Python 3.12 slim image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port FastAPI runs on
EXPOSE 9000

# Command to run the application
CMD ["python3", "main.py"]
