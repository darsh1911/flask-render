# Use an official Python runtime as the base image
FROM --platform=linux/arm64 python:alpine

# Set the working directory in the container to /app
WORKDIR /

# Copy the current directory (our Flask app) into the container at /app
COPY . /

# Install Flask and other dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available for the app
EXPOSE 5000

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]