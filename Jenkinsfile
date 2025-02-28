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
    // agent any
    // {
//         kubernetes {
//             yaml '''
// apiVersion: v1
// kind: Pod
// metadata:
//   labels:
//     app: jenkins-agent
// spec:
//   containers:
//     - name: jnlp
//       image: jenkins/inbound-agent
//       args: ["${computer.jnlpmac}", "${computer.name}"]
//     - name: docker
//       image: docker:latest
//       command: [ "sleep", "infinity" ]
//       volumeMounts:
//         - name: dockersock
//           mountPath: /var/run/docker.sock
//   volumes:
//     - name: dockersock
//       hostPath:
//         path: /var/run/docker.sock
// '''
//         }
//     }
    
    environment {
        AWS_REGION = 'ap-south-1'
        REGISTRY = '216084506783.dkr.ecr.ap-south-1.amazonaws.com'
        REPOSITORY = 'backstract_apps'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
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
                    sh "aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t $REGISTRY/$REPOSITORY:$IMAGE_TAG .
                    docker push $REGISTRY/$REPOSITORY:$IMAGE_TAG
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