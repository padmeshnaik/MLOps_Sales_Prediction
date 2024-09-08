from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import boto3
import pandas as pd
import os

def download_data_from_s3():
    s3 = boto3.client('s3')
    s3.download_file('big-mart-sales-data', 'raw_data/train.csv', '/tmp/train.csv')
    s3.download_file('big-mart-sales-data', 'raw_data/test.csv', '/tmp/test.csv')

def preprocess_data():
    df = pd.read_csv('/tmp/train.csv')
    df.fillna(0, inplace=True)
    df.to_csv('/tmp/preprocessed_train.csv', index=False)

def upload_preprocessed_data_to_s3():
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/preprocessed_train.csv', 'big-mart-sales-data', 'processed_data/preprocessed_train.csv')

def train_model():
    from sklearn.ensemble import RandomForestRegressor
    import pickle

    df = pd.read_csv('/tmp/preprocessed_train.csv')
    X = df[['Item_MRP', 'Item_Weight','Outlet_Establishment_Year']]  # Define your features
    y = df['Item_Outlet_Sales']  # Define your target

    model = RandomForestRegressor()
    model.fit(X, y)

    with open('/tmp/model.pkl', 'wb') as f:
        pickle.dump(model, f)

def upload_model_to_s3():
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/model.pkl', 'big-mart-sales-data', 'models/model.pkl')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('ml_pipeline', default_args=default_args, schedule_interval=timedelta(days=1))

download_task = PythonOperator(
    task_id='download_data_from_s3',
    python_callable=download_data_from_s3,
    dag=dag
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

upload_preprocessed_task = PythonOperator(
    task_id='upload_preprocessed_data_to_s3',
    python_callable=upload_preprocessed_data_to_s3,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

upload_model_task = PythonOperator(
    task_id='upload_model_to_s3',
    python_callable=upload_model_to_s3,
    dag=dag
)

download_task >> preprocess_task >> upload_preprocessed_task >> train_task >> upload_model_task
