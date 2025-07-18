#!/bin/sh

# Generate config based on environment variables
echo "Generating config with VITE_API_URL: ${VITE_API_URL}"

# use envsubst to replace variables in the template
envsubst </usr/share/nginx/html/config-template.js >/usr/share/nginx/html/config.js

echo "Configuration generated successfully."

# Iniciar nginx
echo "Initializing nginx..."
nginx -g "daemon off;"
