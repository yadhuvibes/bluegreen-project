pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
        CONTAINER_GREEN = "green"
        APP_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yadhuvibes/bluegreen-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bluegreen-app .'
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                docker rm -f green || true
                docker run -d --name green -p 5002:5000 bluegreen-app
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                sleep 10
                curl http://localhost:5002
                '''
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                sh '''
                aws elbv2 modify-listener \
                --listener-arn arn:aws:elasticloadbalancing:ap-south-1:652253417155:loadbalancer/app/bluegreen-alb/32c8178b06f72be7 \
                --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-green/2d845c57aff6e61a
                '''
            }
        }
    }

    post {
        failure {
            sh '''
            echo "Rollback triggered"
            docker rm -f green || true

            aws elbv2 modify-listener \
            --listener-arn YOUR_LISTENER_ARN \
            --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-blue/1f37706423e0c648
            '''
        }
    }
}

