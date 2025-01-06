# Use Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5003
EXPOSE 5003

# Run the application
CMD ["python", "capital_gains.py"]

# Set an environment variable for the API key
ENV NINJA_API_KEY="vopFoYntOSunu9wOgno8UQ==6N9s5bNi9ndGWM5I"