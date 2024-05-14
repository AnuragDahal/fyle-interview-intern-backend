# Use an official Python runtime as a parent image
FROM python:3.8.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variable
ENV FLASK_ENV=development

# Run the command to start the server
CMD ["python", "run.py"]