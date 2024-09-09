FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask app files
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
