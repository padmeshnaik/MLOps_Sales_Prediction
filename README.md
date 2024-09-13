# MLOps_Sales_Prediction

MLOps Pipeline for Machine Learning Model Deployment
Project Overview
This project demonstrates a complete MLOps pipeline designed to automate the training, deployment, and monitoring of machine learning models. The pipeline leverages tools such as Jenkins, Docker, Apache Airflow, MLflow, and Kubernetes to streamline model management, version control, and ensure continuous delivery in production environments.

Key Features:

CI/CD Integration: The pipeline integrates with Jenkins to automate the training, testing, and deployment of models. Jenkins orchestrates the entire workflow, from pulling the latest code to deploying models in production environments.
Containerization: The use of Docker ensures that all components (MLflow, Flask application, Airflow, etc.) are containerized, providing a consistent environment across different stages of development.
Model Management: Models are trained and tracked with MLflow for version control and experiment tracking. Models can be deployed and monitored with easy rollback to previous versions if necessary.
Orchestration with Airflow: Apache Airflow is used to orchestrate the entire workflow, including data ingestion, model training, and model deployment tasks. DAGs are set up to automate different stages of the machine learning lifecycle.
AWS Integration: The project integrates with AWS S3 for storage of training data and model artifacts. 
Real-time Data Pipelines: Supports the real-time ingestion of data for model retraining and evaluation, ensuring that the model stays updated with the latest available data.
Monitoring and Logging: Comprehensive logging and monitoring using MLflow and Airflow’s built-in monitoring tools, enabling quick issue resolution and model performance tracking.


├── airflow-docker     
│   ├── dags                                         # Airflow DAGs for pipeline automation     
│   ├── Dockerfile                 # Dockerfile for Airflow setup     
│   └── requirements.txt           # Python dependencies for Airflow      
├── flask-app      
│   ├── app.py                     # Flask application for serving model predictions     
│   ├── Dockerfile                 # Dockerfile for Flask app     
│   └── requirements.txt           # Python dependencies for Flask app     
├── mlflow       
│   ├── Dockerfile                 # Dockerfile for MLflow setup      
│   └── experiment_tracking.py     # Script for managing model training and tracking with MLflow      
├── Jenkinsfile                    # Jenkins pipeline definition      
└── README.md                      # Project documentation     


Prerequisites
Docker and Docker Compose installed on your local machine.
AWS Account with access to S3.
Jenkins installed and configured for CI/CD.
MLflow, Apache Airflow, and Flask Docker images.
Kubernetes Cluster (For container orchestration).
