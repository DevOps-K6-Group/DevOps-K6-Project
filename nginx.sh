#!/bin/bash

# Copy config file (using -f to overwrite if exists)
sudo cp -f app.conf /etc/nginx/sites-available/app.conf

# Remove the default site link to prevent potential conflicts
sudo rm -f /etc/nginx/sites-enabled/default

# Force create the symbolic link (overwrites if it already exists)
sudo ln -sf /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf

# Set workspace permissions
chmod 710 /var/lib/jenkins/workspace/swapit-cicd # Make sure this path is correct

# Test the configuration BEFORE applying it
sudo nginx -t
if [ $? -ne 0 ]; then
  echo "Nginx configuration test failed!"
  exit 1 # Stop the script if config is broken
fi

# Reload Nginx to apply changes; if reload fails, try restarting
sudo systemctl reload nginx || sudo systemctl restart nginx
if [ $? -ne 0 ]; then
  echo "Nginx reload/restart failed!"
  exit 1 # Stop the script if Nginx can't be reloaded/restarted
fi

# Ensure Nginx starts on boot
sudo systemctl enable nginx

echo "Nginx configuration applied and service reloaded/restarted successfully"

# Display status
sudo systemctl status nginx --no-pager
