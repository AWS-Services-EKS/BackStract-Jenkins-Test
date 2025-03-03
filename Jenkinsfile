pipeline {
    agent {
        kubernetes {
            cloud 'BackStract-K8s-Cluster'
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: jnlp
      image: suyashmishra19/jenkins-agent:latest
      args: ['$(JENKINS_SECRET)', '$(JENKINS_NAME)']
      tty: true
      securityContext:
        privileged: true
    - name: docker
      image: docker:20.10.24-dind
      tty: true
      securityContext:
        privileged: true
'''
        }
    }

    environment {
        AWS_REGION = 'ap-south-1'
        REGISTRY = '216084506783.dkr.ecr.ap-south-1.amazonaws.com'
        REPOSITORY = 'backstract_apps'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Debugging') {
            steps {
                sh """
                echo "PATH: $PATH"
                which docker || echo 'Docker not found'
                which aws || echo 'AWS CLI not found'
                ls -lah /usr/bin/docker
                ls -lah /usr/local/bin/aws
                whoami
                groups
                """
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'backstract-aws-creds'
                ]]) {
                    sh """
                    /usr/local/bin/aws ecr get-login-password --region ${env.AWS_REGION} | /usr/bin/docker login --username AWS --password-stdin ${env.REGISTRY}
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh """
                    /usr/bin/docker build -t ${env.REGISTRY}/${env.REPOSITORY}:${env.IMAGE_TAG} .
                    /usr/bin/docker push ${env.REGISTRY}/${env.REPOSITORY}:${env.IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh """
                    kubectl apply -f infra/k8s/deployment.yaml
                    kubectl apply -f infra/k8s/service.yaml
                    kubectl rollout restart deployment backstract-deployment
                    """
                }
            }
        }
    }
}
