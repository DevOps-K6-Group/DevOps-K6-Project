#!/bin/bash

source venv/bin/activate


cd /var/lib/jenkins/workspace/swapit-cicd/currency_converter

python3 manage.py makemigrations
python3 manage.py migrate

echo "Migrations applied successfully"

cd /var/lib/jenkins/workspace/swapit-cicd/

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"


sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "Gunicorn started successfully"

sudo systemctl status gunicorn
sudo systemctl restart gunicorn
