pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/padmeshnaik/MLOps_Sales_Prediction.git'  // Your GitHub repo
        DOCKER_IMAGE = 'mlops-airflow-image'
        ECR_REPOSITORY_URI = '585768184727.dkr.ecr.us-east-1.amazonaws.com/mlops-airflow'  // Replace with your ECR repo URI
        AWS_REGION = 'us-east-1'  // Update with your region
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Load .env file') {
            steps {
                script {
                    def envFile = readFile('~/MLOPS_pipeline/airflow-docker/.env')  // Replace with actual path to your .env file
                    envFile.split('\n').each { line ->
                        if (line.trim()) {
                            def keyVal = line.split('=')
                            env[keyVal[0].trim()] = keyVal[1].trim()
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}", '-f ./Dockerfile .')
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}
                    """
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh """
                    docker tag ${DOCKER_IMAGE}:latest ${ECR_REPOSITORY_URI}:latest
                    docker push ${ECR_REPOSITORY_URI}:latest
                    """
                }
            }
        }

        stage('Trigger Airflow DAG') {
            steps {
                script {
                    sh """
                    curl -X POST 'http://localhost:8080/api/v1/dags/ml_pipeline/dagRuns' \
                    --header 'Content-Type: application/json' \
                    --data '{
                        "dag_run_id": "jenkins_trigger_$(date +%Y%m%d%H%M%S)"
                    }'
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
