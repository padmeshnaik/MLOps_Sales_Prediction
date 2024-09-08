pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/your-repo/mlops-pipeline.git'  // Replace with your GitHub repo
        DOCKER_IMAGE = 'mlops-airflow'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}", './airflow')
                }
            }
        }

        stage('Deploy Airflow') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
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
