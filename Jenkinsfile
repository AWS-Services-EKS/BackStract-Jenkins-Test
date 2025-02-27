pipeline {
    agent {
        kubernetes {
            cloud 'BackStract-K8s-Cluster'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
  - name: docker
    image: docker:20.10.16
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
  """
        }
    }

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '216084506783.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'backstract_apps'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/AWS-Services-EKS/BackStract-Jenkins-Test.git'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                container('docker') {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                container('docker') {
                    sh """
                    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
                    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Configure Kubernetes') {
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh 'kubectl config set-context --current --namespace=default'
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                    sh """
                    kubectl apply -f infra/k8s/deployment.yaml
                    kubectl apply -f infra/k8s/service.yaml
                    kubectl rollout restart deployment backstract-app
                    """
                }
            }
        }
    }
}

