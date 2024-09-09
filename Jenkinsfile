pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mlops-airflow-image'  // Your Docker image name
        AWS_REGION = credentials('aws-region')  // Jenkins credentials for AWS region
        ECR_REPO_URI = credentials('ecr-repo-uri')  // Jenkins credentials for ECR repository URI
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')  // Jenkins credentials for AWS Access Key
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')  // Jenkins credentials for AWS Secret Key
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/padmeshnaik/MLOps_Sales_Prediction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}", '-f airflow-docker/Dockerfile .')
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    // Log in to AWS ECR
                    sh '''
                    aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                    aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                    aws configure set region ${AWS_REGION}
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
                    '''
                }
            }
        }


        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh 'docker tag ${DOCKER_IMAGE}:latest ${ECR_REPO_URI}:latest'
                    sh 'docker push ${ECR_REPO_URI}:latest'
                }
            }
        }

        stage('Trigger Airflow DAG') {
    steps {
        script {
            sh """
            curl -X POST --user padmesh:Neo1947\\$ \
            http://localhost:8081/api/v1/dags/ml_pipeline/dagRuns \
            --header "Content-Type: application/json" \
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
