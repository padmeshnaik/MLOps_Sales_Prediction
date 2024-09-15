pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'mlops-airflow-image'  // Your Docker image name
        MLFLOW_IMAGE = 'mlflow-image'  // MLflow Docker image name
        FLASK_IMAGE = 'flask-app-image'  // Flask Docker image name
        AWS_REGION = credentials('aws-region')  // Jenkins credentials for AWS region
        ECR_REPO_URI = credentials('ecr-repo-uri')  // Jenkins credentials for ECR repository URI
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')  // Jenkins credentials for AWS Access Key
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')  // Jenkins credentials for AWS Secret Key
        EMAIL_RECIPIENTS = 'padmeshnaik22@gmail.com'    
        USERNAME = credentials('username')  
        PASSWORD = credentials('password')
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

            stage('Run MLflow UI') {
                steps {
                    script {
                        sh '''
                        # Stop and remove the existing MLflow container if it's running or stopped
                        CONTAINER_ID=$(docker ps -aq --filter "name=mlflow-container")
                        if [ "$CONTAINER_ID" ]; then
                            docker stop $CONTAINER_ID
                            docker rm $CONTAINER_ID
                        fi

                        # Run the new MLflow UI container
                        docker run -d --network mlops-network --name mlflow-container -p 5002:5000 my-mlflow
                        '''
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


        stage('Push Docker Images to ECR') {
            steps {
                script {
                    // Tag and Push the Airflow image
                    sh 'docker tag ${DOCKER_IMAGE}:latest ${ECR_REPO_URI}:airflow-latest'
                    sh 'docker push ${ECR_REPO_URI}:airflow-latest'

                    // Tag and Push the MLflow image
                    sh 'docker tag ${MLFLOW_IMAGE}:latest ${ECR_REPO_URI}:mlflow-latest'
                    sh 'docker push ${ECR_REPO_URI}:mlflow-latest'

                    // Tag and Push the Flask image
                    sh 'docker tag ${FLASK_IMAGE}:latest ${ECR_REPO_URI}:flask-latest'
                    sh 'docker push ${ECR_REPO_URI}:flask-latest'
                }
            }
        }

        stage('Trigger Airflow DAG') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'airflow-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                            script {
                                sh '''
                                curl -X POST --user ${USERNAME}:${PASSWORD} \
                                http://localhost:8081/api/v1/dags/ml_pipeline/dagRuns \
                                --header "Content-Type: application/json" \
                                --data '{
                                    "conf": {}
                                }'
                                '''
                            }
                        }
                    }
        }


        stage('Stop Existing Flask Container') {
            steps {
                script {
                    // Stop the existing container if running
                    sh '''
                    CONTAINER_ID=$(docker ps -q --filter "ancestor=flask-app-image")
                    if [ "$CONTAINER_ID" ]; then
                        docker stop $CONTAINER_ID
                        docker rm $CONTAINER_ID
                    fi
                    '''
                }
            }
        }

        stage('Build and Run Flask App') {
            steps {
                script {
                    sh '''
                    docker build -t flask-app-image -f flask-app/Dockerfile .
                    docker run -d -p 5000:5000 \
                        -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                        -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                        flask-app-image
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
        
        success {
            emailext (
                subject: "Jenkins Build Success: ${currentBuild.fullDisplayName}",
                body: """<p>The build was successful!</p>
                          <p>Check details at <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                to: "${EMAIL_RECIPIENTS}"
            )
        }
        failure {
            emailext (
                subject: "Jenkins Build Failed: ${currentBuild.fullDisplayName}",
                body: """<p>Unfortunately, the build failed.</p>
                          <p>Check console output at <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                to: "${EMAIL_RECIPIENTS}"
            )
        }
    }
    
}