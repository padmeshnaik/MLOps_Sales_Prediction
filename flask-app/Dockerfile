FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt file first to leverage Docker cache if dependencies don't change
COPY flask-app/requirements.txt /app/requirements.txt

# Install the required Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the Flask app files into the container
COPY flask-app/ /app/

# Set environment variables if needed (e.g., for AWS credentials, Flask environment)
# ENV FLASK_ENV=development

# Run the Flask app
CMD ["python", "app.py"]
