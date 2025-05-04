#!/bin/bash

sudo cp -rf app.conf /etc/nginx/sites-available/

sudo ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/

chmod 710 /var/lib/jenkins/workspace/swapit-cicd

sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx started successfully"

sudo systemctl status nginx


