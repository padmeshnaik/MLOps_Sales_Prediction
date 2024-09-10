# Use a Python base image
FROM python:3.9-slim

# Install MLflow
RUN pip install mlflow

# Expose the port MLflow UI will run on
EXPOSE 5000

# Start MLflow UI
CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"]
