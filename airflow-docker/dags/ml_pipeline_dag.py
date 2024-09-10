from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import boto3
import pandas as pd
import pickle
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor

# S3 Config
S3_BUCKET = 'big-mart-sales-data'
TRAIN_DATA_KEY = 'raw_data/train.csv'
PROCESSED_DATA_KEY = 'processed_data/preprocessed_train_v{version}.csv'
MODEL_FILE_KEY = 'models/model_v{version}.pkl'
LOCAL_TRAIN_PATH = '/tmp/train.csv'
LOCAL_PREPROCESSED_PATH = '/tmp/preprocessed_train.csv'
LOCAL_MODEL_PATH = '/tmp/model.pkl'


# Initialize version counters for both data and model
DATA_VERSION = 1  # This can be dynamically tracked
MODEL_VERSION = 1  # This can be dynamically tracked

# Define Functions for each step in the pipeline

def download_data_from_s3():
    s3 = boto3.client('s3')
    s3.download_file(S3_BUCKET, TRAIN_DATA_KEY, LOCAL_TRAIN_PATH)

def preprocess_data():
    # Load and preprocess data
    df = pd.read_csv(LOCAL_TRAIN_PATH)
    df.fillna(0, inplace=True)  # Fill missing values
    df.to_csv(LOCAL_PREPROCESSED_PATH, index=False)

def upload_preprocessed_data_to_s3():
    s3 = boto3.client('s3')
    global DATA_VERSION
    versioned_key = PROCESSED_DATA_KEY.format(version=DATA_VERSION)
    s3.upload_file(LOCAL_PREPROCESSED_PATH, S3_BUCKET, versioned_key)
    DATA_VERSION += 1  # Increment the version after each upload

def train_model():
    # Load the preprocessed data
    mlflow.set_tracking_uri("http://172.17.0.1:5002")

    df = pd.read_csv(LOCAL_PREPROCESSED_PATH)
    X = df[['Item_MRP', 'Item_Weight', 'Outlet_Establishment_Year']]  # Define your features
    y = df['Item_Outlet_Sales']  # Define your target

    # Start MLflow run for tracking
    with mlflow.start_run():
        # Train the model
        model = RandomForestRegressor()
        model.fit(X, y)

        # Log model parameters and metrics
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_metric("training_samples", len(X))

        # Save the model
        with open(LOCAL_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)

        # Log the model as an artifact in MLflow
        mlflow.sklearn.log_model(model, "model")

def upload_model_to_s3():
    # Upload the trained model to S3 with versioning
    s3 = boto3.client('s3')
    global MODEL_VERSION
    versioned_key = MODEL_FILE_KEY.format(version=MODEL_VERSION)
    s3.upload_file(LOCAL_MODEL_PATH, S3_BUCKET, versioned_key)
    MODEL_VERSION += 1  # Increment the model version after each upload

# Airflow DAG and task definitions
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_pipeline',  # DAG name
    default_args=default_args,
    catchup=False,
    schedule_interval=None  # This DAG is triggered manually, not on a schedule
)

# Define Airflow tasks

# Task to download the raw data from S3
download_task = PythonOperator(
    task_id='download_data_from_s3',
    python_callable=download_data_from_s3,
    dag=dag
)

# Task to preprocess the data
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

# Task to upload the preprocessed data back to S3 with versioning
upload_preprocessed_task = PythonOperator(
    task_id='upload_preprocessed_data_to_s3',
    python_callable=upload_preprocessed_data_to_s3,
    dag=dag
)

# Task to train the model and track the experiment using MLflow
train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

# Task to upload the trained model to S3 with versioning
upload_model_task = PythonOperator(
    task_id='upload_model_to_s3',
    python_callable=upload_model_to_s3,
    dag=dag
)

# Define task dependencies in the pipeline
download_task >> preprocess_task >> upload_preprocessed_task >> train_task >> upload_model_task
