# Use the official Python 3.14 slim image
FROM python:3.14-rc-slim

# Set the working directory inside the container
WORKDIR /app

# Install Flask 
RUN pip install --upgrade pip && pip install Flask==3.0.3

# Copy the application code into the container
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["flask", "run"]
