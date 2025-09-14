#!/bin/bash

# Production deployment script for Kapiga Research Site
# This script builds and pushes your Docker image to Docker Hub, then prints Render.com deployment instructions.

set -e

IMAGE_NAME=willboyden/kapiga-research-site:latest
REPO_URL=https://github.com/willboyden/kapiga-research-site

echo "🚀 Building Docker image..."
docker build -t $IMAGE_NAME .
echo "Docker image built: $IMAGE_NAME"

echo "🚀 Pushing Docker image to Docker Hub..."
docker push $IMAGE_NAME
echo "Docker image pushed."

echo "\n--- Render.com Deployment Instructions ---"
echo "1. Go to https://dashboard.render.com and create a new Web Service."
echo "2. Select 'Deploy from Docker Hub' and use: $IMAGE_NAME"
echo "3. Set environment variables from your .env.example (especially DATABASE_URL, SECRET_KEY, etc)."
echo "4. Create a Postgres database in Render and copy its DATABASE_URL."
echo "5. Set up auto-deploy from your GitHub repo if desired."
echo "6. Click 'Create Web Service' to deploy."
echo "---"

echo "Done! Your app is ready for production deployment."

# Run migrations
echo "Running database migrations..."
docker compose -f docker-compose.production.yml exec web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput

# Create superuser (optional)
echo "Creating admin user (optional)..."
docker compose -f docker-compose.production.yml exec web python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'changeme123')
    print('Admin user created: admin/changeme123')
"

echo "🎉 Deployment complete!"
echo "📊 Access your site at: http://$(curl -s ifconfig.me)"
echo "🔧 Admin panel: http://$(curl -s ifconfig.me)/admin"
echo "📈 Jupyter notebooks: http://$(curl -s ifconfig.me):8888"

# Show running containers
docker compose -f docker-compose.production.yml ps
