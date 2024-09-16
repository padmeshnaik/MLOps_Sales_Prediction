pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'mlops-airflow-image'
        MLFLOW_IMAGE = 'mlflow-image'
        FLASK_IMAGE = 'flask-app-image'
        AWS_REGION = credentials('aws-region')
        ECR_REPO_URI = credentials('ecr-repo-uri')
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        EMAIL_RECIPIENTS = 'padmeshnaik22@gmail.com'
        USERNAME = credentials('username')
        PASSWORD = credentials('password')
        KUBECONFIG = '/home/padmesh/.kube/config'  // Path to kubeconfig
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/padmeshnaik/MLOps_Sales_Prediction.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}", '--no-cache -f airflow-docker/Dockerfile .')
                    docker.build("${MLFLOW_IMAGE}", '--no-cache -f Dockerfile .')
                    docker.build("${FLASK_IMAGE}", '--no-cache -f flask-app/Dockerfile .')
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh '''
                    aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                    aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                    aws configure set region ${AWS_REGION}
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
                    '''
                }
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                script {
                    sh '''
                    docker tag ${DOCKER_IMAGE}:latest ${ECR_REPO_URI}:airflow-latest
                    docker push ${ECR_REPO_URI}:airflow-latest
                    docker tag ${MLFLOW_IMAGE}:latest ${ECR_REPO_URI}:mlflow-latest
                    docker push ${ECR_REPO_URI}:mlflow-latest
                    docker tag ${FLASK_IMAGE}:latest ${ECR_REPO_URI}:flask-latest
                    docker push ${ECR_REPO_URI}:flask-latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use KUBECONFIG to ensure kubectl uses the correct config
                    sh '''
                    export KUBECONFIG=${KUBECONFIG}
                    kubectl apply -f k8s/mlflow-deployment.yaml
                    kubectl apply -f k8s/flask-deployment.yaml
                    kubectl apply -f k8s/airflow-deployment.yaml
                    '''
                }
            }
        }
    }

    post {
        always {
            emailext (
                subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
                body: """<p>Build Status: ${currentBuild.currentResult}</p>
                          <p>Check console output at <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                to: "${EMAIL_RECIPIENTS}"
            )
        }
    }
}
