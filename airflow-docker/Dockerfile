FROM apache/airflow:2.5.0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt from the airflow directory into the container
COPY airflow-docker/requirements.txt /app/requirements.txt


# Install the Python dependencies
# Install dependencies using the correct pip linked to the global Python environment
RUN /usr/local/bin/python -m pip install --no-cache-dir -r /app/requirements.txt

# Copy DAGs into the container
COPY airflow-docker/dags /opt/airflow/dags

