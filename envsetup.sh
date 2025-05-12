
#!/bin/bash

# This script sets up the environment for the project by creating a virtual environment and installing dependencies.

VENV_DIR="venv"
LOG_DIR="logs"

# Create virtual environment if it doesn't exist
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists. Skipping creation."
else
    echo "Creating virtual environment '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment *for this script's context*
echo "Activating virtual environment for script execution..."
. "$VENV_DIR/bin/activate"

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies."
        # Consider exiting if dependencies are critical: exit 1
    fi
else
    echo "WARNING: requirements.txt not found. Skipping dependency installation."
fi

# Create log directory and files if they don't exist
if [ -d "$LOG_DIR" ]; then
    echo "Log folder '$LOG_DIR' already exists."
else
    echo "Creating log folder '$LOG_DIR'..."
    mkdir "$LOG_DIR"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create log directory."
        exit 1
    fi
fi

# Create log files if they don't exist
touch "$LOG_DIR/error.log" "$LOG_DIR/access.log"

# Set appropriate permissions 
echo "Setting permissions for '$LOG_DIR'..."
chmod -R 777 "$LOG_DIR" 

echo "Environment setup script finished."
echo "To activate the virtual environment in your current shell, run: source $VENV_DIR/bin/activate"

# Deactivate is automatic when script exits, but good practice if script continued
# deactivate
