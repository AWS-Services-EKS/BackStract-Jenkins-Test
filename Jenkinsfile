pipeline {
    agent {
        kubernetes {
            cloud 'BackStract-K8s-Cluster'
        }
    }
//     agent {
//         kubernetes {
//             cloud 'BackStract-K8s-Cluster'
//             yaml """
// apiVersion: v1
// kind: Pod
// spec:
//   containers:
//   - name: jnlp
//     image: jenkins/inbound-agent:latest
//     command:
//     - cat
//     tty: true
//   """
//         }
//     }

    environment {
        AWS_REGION = 'ap-south-1'
        REGISTRY = '216084506783.dkr.ecr.ap-south-1.amazonaws.com'
        REPOSITORY = 'backstract_apps'
        IMAGE_TAG = "${env.BUILD_NUMBER}"  // ✅ Fixed missing closing quote
    }

    stages {
        stage('Check AWS CLI & Docker') {
        steps {
            sh 'aws --version'
            sh 'docker --version'
        }
    }

        // stage('Check AWS CLI & Docker') {
        //     steps {
        //         sh 'aws --version'
        //         sh 'docker --version'
        //     }
        // }

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
