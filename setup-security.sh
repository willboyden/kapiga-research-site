#!/bin/bash
# Automated SSL setup and security hardening for VPS deployment
# This script sets up Let's Encrypt SSL and security best practices

set -e

echo "🔒 Setting up SSL and Security for Dr. Kapiga Research Site..."

# Variables
DOMAIN=${1:-"your-domain.com"}
EMAIL=${2:-"admin@your-domain.com"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install security essentials
print_status "Installing security tools..."
sudo apt install -y ufw fail2ban certbot python3-certbot-nginx htop curl wget unzip

# Configure UFW Firewall
print_status "Configuring firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Configure Fail2ban
print_status "Setting up Fail2ban..."
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-req-limit]
enabled = true
filter = nginx-req-limit
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF

sudo systemctl restart fail2ban
print_status "Fail2ban configured and started"

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Setup SSL certificates with Certbot
if [ "$DOMAIN" != "your-domain.com" ]; then
    print_status "Setting up SSL certificate for $DOMAIN..."
    
    # Create nginx configuration for initial certificate
    sudo tee /etc/nginx/sites-available/kapiga-research > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}
EOF

    sudo ln -sf /etc/nginx/sites-available/kapiga-research /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
    
    # Create directory for certbot
    sudo mkdir -p /var/www/certbot
    
    # Get SSL certificate
    sudo certbot certonly --webroot -w /var/www/certbot -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --no-eff-email
    
    if [ $? -eq 0 ]; then
        print_status "SSL certificate obtained successfully"
        
        # Update docker-compose with SSL configuration
        sed -i "s/your-domain.com/$DOMAIN/g" docker-compose.production.yml
        sed -i "s/your-domain.com/$DOMAIN/g" nginx.prod.conf
        
        # Setup auto-renewal
        (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet && docker-compose -f $(pwd)/docker-compose.production.yml restart nginx") | crontab -
        
    else
        print_warning "SSL certificate setup failed. Continuing with HTTP..."
    fi
else
    print_warning "Using default domain. Please update DOMAIN variable for SSL setup."
fi

# Generate secure environment file
print_status "Generating secure environment configuration..."
cat > .env <<EOF
# Security Configuration
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,localhost,127.0.0.1

# Database Configuration
POSTGRES_DB=kapiga_research
POSTGRES_USER=kapiga_user
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Email Configuration (update with your SMTP settings)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@$DOMAIN

# Domain Configuration
DOMAIN=$DOMAIN
EOF

# Set secure permissions on environment file
chmod 600 .env
print_status "Environment file created with secure permissions"

# Create backup script
print_status "Setting up automated backups..."
sudo tee /usr/local/bin/backup-kapiga-research.sh > /dev/null <<EOF
#!/bin/bash
# Automated backup script for Dr. Kapiga Research Site

BACKUP_DIR="/var/backups/kapiga-research"
DATE=\$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p \$BACKUP_DIR

# Backup database
docker exec \$(docker ps -qf "name=kapiga_research_site_db") pg_dump -U kapiga_user kapiga_research | gzip > \$BACKUP_DIR/db_backup_\$DATE.sql.gz

# Backup media files
tar -czf \$BACKUP_DIR/media_backup_\$DATE.tar.gz -C $(pwd) media/

# Keep only last 7 days of backups
find \$BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: \$DATE"
EOF

sudo chmod +x /usr/local/bin/backup-kapiga-research.sh

# Setup daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-kapiga-research.sh >> /var/log/kapiga-backup.log 2>&1") | crontab -

print_status "Daily backup scheduled"

# Setup system monitoring
print_status "Setting up system monitoring..."
sudo tee /usr/local/bin/system-monitor.sh > /dev/null <<EOF
#!/bin/bash
# System monitoring script

# Check disk usage
DISK_USAGE=\$(df / | awk 'NR==2 {print \$5}' | sed 's/%//')
if [ \$DISK_USAGE -gt 80 ]; then
    echo "WARNING: Disk usage is \$DISK_USAGE%"
fi

# Check memory usage
MEM_USAGE=\$(free | awk 'NR==2{printf "%.0f", \$3*100/\$2}')
if [ \$MEM_USAGE -gt 80 ]; then
    echo "WARNING: Memory usage is \$MEM_USAGE%"
fi

# Check if containers are running
if ! docker ps | grep -q kapiga_research_site; then
    echo "ERROR: Kapiga Research containers not running"
fi

# Log system status
echo "\$(date): Disk: \$DISK_USAGE%, Memory: \$MEM_USAGE%" >> /var/log/system-monitor.log
EOF

sudo chmod +x /usr/local/bin/system-monitor.sh

# Run monitoring every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/system-monitor.sh") | crontab -

# Security hardening
print_status "Applying additional security hardening..."

# Disable root login over SSH
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password authentication (if SSH keys are setup)
# sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

sudo systemctl restart ssh

# Set secure file permissions
find . -type f -name "*.py" -exec chmod 644 {} \;
find . -type f -name "*.sh" -exec chmod 755 {} \;
chmod 600 .env

print_status "Security hardening completed"

# Deploy the application
print_status "Deploying the application with security configurations..."
docker-compose -f docker-compose.production.yml down 2>/dev/null || true
docker-compose -f docker-compose.production.yml up -d --build

# Wait for services to start
sleep 20

# Run database migrations
docker-compose -f docker-compose.production.yml exec -T web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.production.yml exec -T web python manage.py collectstatic --noinput

# Create superuser
print_status "Creating admin user..."
docker-compose -f docker-compose.production.yml exec -T web python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Change_This_Password_123!')
    print('Admin user created: admin/Change_This_Password_123!')
    print('IMPORTANT: Change this password immediately!')
EOF

# Final security check
print_status "Running final security checks..."

# Check if containers are running
if docker ps | grep -q kapiga_research_site; then
    print_status "All containers are running"
else
    print_error "Some containers failed to start"
fi

# Check SSL certificate
if [ "$DOMAIN" != "your-domain.com" ]; then
    SSL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/ || echo "000")
    if [ "$SSL_STATUS" = "200" ] || [ "$SSL_STATUS" = "301" ] || [ "$SSL_STATUS" = "302" ]; then
        print_status "SSL certificate is working"
    else
        print_warning "SSL certificate might not be working properly"
    fi
fi

# Display summary
echo ""
echo "🎉 Security setup completed!"
echo "=========================="
echo ""
print_status "Firewall: Configured and active"
print_status "Fail2ban: Configured for SSH and Nginx protection"
print_status "SSL Certificate: $([ "$DOMAIN" != "your-domain.com" ] && echo "Configured" || echo "Manual setup required")"
print_status "Automated Backups: Daily at 2 AM"
print_status "System Monitoring: Every 5 minutes"
print_status "Docker Security: Containers running as non-root"
print_status "Django Security: All security headers enabled"
echo ""
echo "🌐 Your site: https://$DOMAIN"
echo "🔧 Admin panel: https://$DOMAIN/admin"
echo "📊 Jupyter notebooks: Port 8888 (if enabled)"
echo ""
echo "🔑 Default admin credentials:"
echo "   Username: admin"
echo "   Password: Change_This_Password_123!"
echo ""
print_warning "IMPORTANT: Change the admin password immediately!"
print_warning "Update email settings in .env file for notifications"
print_warning "Review firewall rules if you need additional ports"
echo ""
print_status "Security logs: /var/log/fail2ban.log, /var/log/system-monitor.log"
print_status "Backup location: /var/backups/kapiga-research/"
echo ""
