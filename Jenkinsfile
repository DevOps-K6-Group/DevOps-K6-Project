// This Jenkinsfile is designed to automate the deployment of a Django application
pipeline {
    agent any
    stages {
        stage('Setup Python Virtual Environment') {
            steps {
                echo 'Setting Up Venv...'
                sh '''
                chmod +x envsetup.sh
                ./envsetup.sh
                '''
            }
        }
        
        stage('Collect Static Files') {
            steps {
                echo 'Collecting static files...'
                sh '''
                source venv/bin/activate
                python manage.py collectstatic --noinput --clear
                
                # Ensure proper permissions
                sudo chown -R www-data:www-data /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/
                sudo chmod -R 755 /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/
                
                # Alternative: Move to persistent location (recommended)
                sudo mkdir -p /var/www/static
                sudo rsync -a --delete /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/ /var/www/static/
                '''
            }
        }
        
        stage('Setup Gunicorn Server') {
            steps {
                echo 'Starting Up Gunicorn...'
                sh '''
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }
        
        stage('Setup Nginx Server') {
            steps {
                echo 'Starting Up Nginx...'
                sh '''
                chmod +x nginx.sh
                ./nginx.sh
                
                # Verify static files are accessible
                curl -I http://localhost/static/admin/css/base.css || true
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            sh '''
            # Optional: Remove old static files from Jenkins workspace
            rm -rf /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/
            '''
        }
        success {
            echo 'Deployment successful! Static files should now be served correctly.'
        }
        failure {
            echo 'Deployment failed. Check static files permissions and Nginx configuration.'
        }
    }
}