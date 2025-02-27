pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  - name: aws
    image: amazon/aws-cli:latest
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:1.31.0
    command:
    - cat
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }
    
    environment {
        AWS_REGION = 'ap-south-1'
        EKS_CLUSTER_NAME = 'backstract-dev'
        ECR_REPOSITORY = 'backstract_apps'
        IMAGE_TAG = "${env.GIT_COMMIT}"
        DEPLOYMENT_NAME = 'coll-eb884f03d5454c89a93e004aac77ad26-depl'
        AWS_CREDENTIALS = credentials('aws-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Configure AWS') {
            steps {
                container('aws') {
                    sh '''
                    aws configure set aws_access_key_id $AWS_CREDENTIALS_USR
                    aws configure set aws_secret_access_key $AWS_CREDENTIALS_PSW
                    aws configure set region $AWS_REGION
                    '''
                }
            }
        }
        
        stage('Login to ECR') {
            steps {
                container('aws') {
                    script {
                        def ecrLogin = sh(script: "aws ecr get-login-password --region ${AWS_REGION}", returnStdout: true).trim()
                        env.ECR_REGISTRY = sh(script: "aws ecr describe-repositories --repository-names ${ECR_REPOSITORY} --query 'repositories[0].repositoryUri' --output text", returnStdout: true).trim().split('/')[0]
                        
                        // Pass ECR credentials to the docker container
                        withCredentials([string(credentialsId: 'aws-credentials', variable: 'AWS_CREDS')]) {
                            sh "docker login -u AWS -p ${ecrLogin} ${env.ECR_REGISTRY}"
                        }
                    }
                }
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                container('docker') {
                    sh """
                    docker build -t ${env.ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} -t ${env.ECR_REGISTRY}/${ECR_REPOSITORY}:coll-eb884f03d5454c89a93e004aac77ad26 .
                    docker push ${env.ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    docker push ${env.ECR_REGISTRY}/${ECR_REPOSITORY}:coll-eb884f03d5454c89a93e004aac77ad26
                    """
                }
            }
        }
        
        stage('Update Kubeconfig') {
            steps {
                container('aws') {
                    sh "aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}"
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                    sh """
                    kubectl apply -f infra/k8s/aws-auth.yaml
                    kubectl apply -f infra/k8s/deployment.yaml
                    kubectl apply -f infra/k8s/service.yaml
                    kubectl rollout restart deployment ${DEPLOYMENT_NAME}
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
