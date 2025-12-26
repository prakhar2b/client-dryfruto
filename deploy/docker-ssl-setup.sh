#!/bin/bash

#===========================================
# DryFruto - Docker SSL Setup
# Using Let's Encrypt with Certbot
#===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

APP_DIR="/var/www/dryfruto"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  DryFruto - Docker SSL Setup${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root (use sudo)${NC}"
  exit 1
fi

# Get configuration
read -p "Enter your domain name (e.g., example.com): " DOMAIN
read -p "Enter your email for SSL notifications: " EMAIL

# Install Certbot
echo -e "${YELLOW}Installing Certbot...${NC}"
apt update
apt install -y certbot

# Stop nginx temporarily
echo -e "${YELLOW}Stopping containers...${NC}"
cd $APP_DIR
docker-compose -f docker-compose.prod.yml stop nginx

# Obtain certificate
echo -e "${YELLOW}Obtaining SSL certificate...${NC}"
certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos -m $EMAIL

# Create SSL directory and copy certificates
echo -e "${YELLOW}Setting up SSL certificates...${NC}"
mkdir -p $APP_DIR/docker/ssl
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $APP_DIR/docker/ssl/
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $APP_DIR/docker/ssl/
chmod 600 $APP_DIR/docker/ssl/*.pem

# Update nginx config for SSL
echo -e "${YELLOW}Updating Nginx configuration...${NC}"
cat > $APP_DIR/docker/nginx-proxy.conf << 'EOF'
upstream backend {
    server backend:8001;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name _;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # API proxy
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    # Serve uploaded files
    location /uploads/ {
        alias /var/www/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Serve React app
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Update .env with HTTPS
echo -e "${YELLOW}Updating environment...${NC}"
cat > $APP_DIR/.env << EOF
SITE_URL=https://${DOMAIN}
MONGO_URL=mongodb://mongodb:27017
DB_NAME=dryfruto
EOF

# Rebuild frontend with HTTPS URL
echo -e "${YELLOW}Rebuilding frontend with HTTPS...${NC}"
cd $APP_DIR/frontend
echo "REACT_APP_BACKEND_URL=https://${DOMAIN}" > .env
npm run build
cd ..

# Restart containers
echo -e "${YELLOW}Restarting containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Setup auto-renewal cron job
echo -e "${YELLOW}Setting up auto-renewal...${NC}"
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/$DOMAIN/*.pem $APP_DIR/docker/ssl/ && docker-compose -f $APP_DIR/docker-compose.prod.yml restart nginx") | crontab -

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  SSL Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Your site is now secured with HTTPS: ${YELLOW}https://${DOMAIN}${NC}"
echo -e "SSL certificate will auto-renew before expiration."
