# Single container with nginx, frontend, and backend
FROM python:3.11-slim

# Install nginx, supervisor, and apache2-utils for htpasswd
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    curl \
    apache2-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for backend
WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend files to nginx html directory
COPY frontend/ /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy htpasswd generation script
COPY generate_htpasswd.sh /usr/local/bin/generate_htpasswd.sh
RUN chmod +x /usr/local/bin/generate_htpasswd.sh

# Create nginx log directory
RUN mkdir -p /var/log/nginx

EXPOSE 5555

# Start script that generates htpasswd and then starts supervisor
CMD ["/bin/bash", "-c", "/usr/local/bin/generate_htpasswd.sh \"$ADMIN_PASSWORD\" && /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
