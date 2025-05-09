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
        
        stage('Handle Static Files') {
            steps {
                echo 'Setting up static files...'
                sh '''
                # Use . instead of source (more compatible)
                . venv/bin/activate

                # Navigate to project directory
                cd currency_converter
                
                # Create persistent directory with proper permissions
                sudo mkdir -p /var/www/static
                sudo chown -R jenkins:www-data /var/www/static
                sudo chmod -R 775 /var/www/static
                
                # Collect static files
                python manage.py collectstatic --noinput --clear
                
                # Fix permissions for Nginx
                sudo chown -R www-data:www-data /var/www/static
                sudo chmod -R 755 /var/www/static
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
                
                # Verify static files
                sleep 3
                curl -I http://localhost/static/admin/css/base.css || true
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            sh '''
            # Clean workspace staticfiles as jenkins user
            sudo rm -rf /var/lib/jenkins/workspace/swapit-cicd/currency_converter/staticfiles/ || true
            '''
        }
    }
}