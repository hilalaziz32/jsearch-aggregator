#!/bin/bash

# Generate .htpasswd file for nginx basic authentication
# Usage: ./generate_htpasswd.sh <password>

set -e

if [ -z "$1" ]; then
    echo "Error: Password argument is required"
    echo "Usage: $0 <password>"
    exit 1
fi

PASSWORD="$1"
USERNAME="helm"

# Create the .htpasswd file
echo "Generating .htpasswd file for user: $USERNAME"
htpasswd -bc /etc/nginx/.htpasswd "$USERNAME" "$PASSWORD"

# Verify the file was created
if [ -f "/etc/nginx/.htpasswd" ]; then
    echo "Successfully generated .htpasswd file at /etc/nginx/.htpasswd"
    echo "File contents:"
    cat /etc/nginx/.htpasswd
else
    echo "ERROR: Failed to create .htpasswd file"
    exit 1
fi
