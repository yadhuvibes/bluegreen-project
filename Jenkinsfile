pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"

        BLUE_CONTAINER  = "blue"
        GREEN_CONTAINER = "green"

        BLUE_PORT  = "5001"
        GREEN_PORT = "5002"

        TG_BLUE  = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-blue/1f37706423e0c648"
        TG_GREEN = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:targetgroup/tg-green/2d845c57aff6e61a"

        LISTENER_ARN = "arn:aws:elasticloadbalancing:ap-south-1:652253417155:listener/app/bluegreen-alb/32c8178b06f72be7/9b0831bfef736580"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/yadhuvibes/bluegreen-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bluegreen-app .'
            }
        }

        stage('Deploy GREEN') {
            steps {
                sh '''
                echo "Stopping old GREEN container (if any)..."
                docker rm -f green || true

                echo "Starting GREEN container..."
                docker run -d --name green -p 5002:5000 bluegreen-app
                '''
            }
        }

        stage('Smoke Test GREEN') {
            steps {
                sh '''
                echo "Waiting for GREEN to start..."
                sleep 10

                echo "Testing GREEN app..."
                curl -f http://localhost:5002

                echo "GREEN is healthy ✔"
                '''
            }
        }

        stage('Switch Traffic BLUE → GREEN') {
            steps {
                sh '''
                echo "=============================="
                echo "SWITCHING TRAFFIC TO GREEN"
                echo "=============================="

                aws elbv2 modify-listener \
                --listener-arn $LISTENER_ARN \
                --default-actions Type=forward,TargetGroupArn=$TG_GREEN

                echo "GREEN is now LIVE ✔"
                '''
            }
        }
    }

    post {

        success {
            sh '''
            echo "=============================="
            echo "DEPLOYMENT SUCCESS"
            echo "CURRENT LIVE ENVIRONMENT: GREEN"
            echo "=============================="
            '''
        }

        failure {
            sh '''
            echo "=============================="
            echo "DEPLOYMENT FAILED → ROLLBACK"
            echo "Switching back to BLUE..."
            echo "=============================="

            docker rm -f green || true

            aws elbv2 modify-listener \
            --listener-arn $LISTENER_ARN \
            --default-actions Type=forward,TargetGroupArn=$TG_BLUE

            echo "Rollback completed → BLUE is LIVE"
            '''
        }
    }
}
