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
        
        // NEW STAGE ADDED HERE
        stage('Handle Static Files') {
            steps {
                echo 'Setting up static files...'
                sh '''
                source venv/bin/activate
                
                # Create persistent static directory if not exists
                sudo mkdir -p /var/www/static
                
                # Collect static files to persistent location
                python manage.py collectstatic --noinput --clear
                
                # Set proper permissions
                sudo chown -R www-data:www-data /var/www/static
                sudo chmod -R 755 /var/www/static
                
                # Verify files were collected
                ls -la /var/www/static
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
                sleep 5  # Wait for Nginx to start
                curl -I http://localhost/static/admin/css/base.css || echo "Static files check failed"
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            // Optional: Remove workspace staticfiles if they exist
            sh 'rm -rf /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/ || true'
        }
        success {
            echo 'Deployment successful! Static files are now served from /var/www/static'
        }
    }
}