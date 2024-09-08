pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mlops-airflow-image'  // Your Docker image name
        AWS_REGION = ''  // This will be set from the .env file
        ECR_REPO_URI = ''  // This will be set from the .env file
        AWS_ACCESS_KEY_ID = ''  // This will be set from the .env file
        AWS_SECRET_ACCESS_KEY = ''  // This will be set from the .env file
    }

    stages {
        stage('Load Environment Variables') {
            steps {
                script {
                    def envFile = readFile '.env'
                    def envMap = envFile.split('\n').collectEntries { line ->
                        def parts = line.split('=')
                        [(parts[0]): parts[1].trim()]
                    }

                    // Set environment variables from the .env file
                    AWS_REGION = envMap.AWS_REGION
                    ECR_REPO_URI = envMap.ECR_REPO_URI
                    AWS_ACCESS_KEY_ID = envMap.AWS_ACCESS_KEY_ID
                    AWS_SECRET_ACCESS_KEY = envMap.AWS_SECRET_ACCESS_KEY
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/padmeshnaik/MLOps_Sales_Prediction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${ECR_REPO_URI}:${DOCKER_IMAGE}", '-f airflow-docker/Dockerfile .')
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh """
                    \$(aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI})
                    """
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh 'docker push ${ECR_REPO_URI}:${DOCKER_IMAGE}'
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
                                "dag_run_id": "jenkins_trigger_\\\\$(date +%Y%m%d%H%M%S)"
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
