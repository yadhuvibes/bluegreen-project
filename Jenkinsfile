pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"

        // AWS ARNs (REPLACE ONLY IF YOURS CHANGE)
        LISTENER_ARN = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:listener/app/bluegreen-alb/32c8178b06f72be7/9b0831bfef736580"

        TG_GREEN = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-green/2d845c57aff6e61a"

        TG_BLUE = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-blue/1f37706423e0c648"
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
                curl --retry 5 --retry-delay 3 http://localhost:5002
                '''
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                sh '''
                aws elbv2 modify-listener \
                --listener-arn $LISTENER_ARN \
                --default-actions Type=forward,TargetGroupArn=$TG_GREEN
                '''
            }
        }
    }

    post {
        failure {
            steps {
                sh '''
                echo "Rollback triggered"

                docker rm -f green || true

                aws elbv2 modify-listener \
                --listener-arn $LISTENER_ARN \
                --default-actions Type=forward,TargetGroupArn=$TG_BLUE
                '''
            }
        }
    }
}
