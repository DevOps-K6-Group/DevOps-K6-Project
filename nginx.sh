#!/bin/bash

# Copy config file (using -f to overwrite if exists)
sudo cp -f app.conf /etc/nginx/sites-available/app.conf

sudo rm -f /etc/nginx/sites-enabled/default

sudo ln -sf /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf

# Set workspace permissions
chmod 710 /var/lib/jenkins/workspace/swapit-cicd 

sudo nginx -t
if [ $? -ne 0 ]; then
  echo "Nginx configuration test failed!"
  exit 1 
fi

sudo systemctl reload nginx || sudo systemctl restart nginx
if [ $? -ne 0 ]; then
  echo "Nginx reload/restart failed!"
  exit 1 
fi

# Ensure Nginx starts on boot
sudo systemctl enable nginx

echo "Nginx configuration applied and service reloaded/restarted successfully"

# Display status
sudo systemctl status nginx --no-pager
