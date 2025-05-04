#!/bin/bash

# Define source and destination paths
CONFIG_SOURCE="app.conf" # Assuming app.conf is in the workspace root
SITES_AVAILABLE_DIR="/etc/nginx/sites-available"
SITES_ENABLED_DIR="/etc/nginx/sites-enabled"
CONFIG_NAME="app.conf" # The name of the config file in sites-* directories
CONF_D_DIR="/etc/nginx/conf.d"
WORKSPACE_DIR="/var/lib/jenkins/workspace/swapit-cicd" # Make sure this matches your actual workspace

echo "--- Setting up Nginx ---"

# 1. Copy the configuration file to sites-available
echo "Copying $CONFIG_SOURCE to $SITES_AVAILABLE_DIR/$CONFIG_NAME"
sudo cp -f "$CONFIG_SOURCE" "$SITES_AVAILABLE_DIR/$CONFIG_NAME"
if [ $? -ne 0 ]; then echo "Error copying config file"; exit 1; fi

# 2. Remove potential duplicate config from conf.d (just in case)
echo "Removing potential duplicate $CONF_D_DIR/$CONFIG_NAME"
sudo rm -f "$CONF_D_DIR/$CONFIG_NAME"

# 3. Remove the default Nginx site configuration link if it exists
echo "Removing default site link $SITES_ENABLED_DIR/default"
sudo rm -f "$SITES_ENABLED_DIR/default"

# 4. Force-create the symbolic link in sites-enabled (overwrites if exists)
echo "Creating symlink $SITES_ENABLED_DIR/$CONFIG_NAME -> $SITES_AVAILABLE_DIR/$CONFIG_NAME"
sudo ln -sf "$SITES_AVAILABLE_DIR/$CONFIG_NAME" "$SITES_ENABLED_DIR/$CONFIG_NAME"
if [ $? -ne 0 ]; then echo "Error creating symlink"; exit 1; fi

# 5. Adjust workspace permissions (ensure correct path)
echo "Setting permissions for $WORKSPACE_DIR"
sudo chmod 710 "$WORKSPACE_DIR"
# Consider if specific subdirectories need different permissions for Nginx/Gunicorn

# 6. Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t
if [ $? -ne 0 ]; then echo "Nginx configuration test failed!"; exit 1; fi

# 7. Reload Nginx to apply configuration changes (more graceful than restart/start)
echo "Reloading Nginx service..."
sudo systemctl reload nginx
if [ $? -ne 0 ]; then
  echo "Nginx reload failed, attempting restart..."
  sudo systemctl restart nginx
  if [ $? -ne 0 ]; then echo "Nginx restart also failed!"; exit 1; fi
fi

# 8. Ensure Nginx service is enabled to start on boot
echo "Enabling Nginx service..."
sudo systemctl enable nginx

echo "--- Nginx setup completed successfully ---"

# 9. Display Nginx status (optional, but good for logging)
echo "Current Nginx status:"
sudo systemctl status nginx --no-pager
