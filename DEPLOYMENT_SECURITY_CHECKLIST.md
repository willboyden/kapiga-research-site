# 🔒 Production Deployment Security Checklist

## Pre-Deployment Security Checklist

### Environment & Secrets
- [ ] Generated new SECRET_KEY using Django command
- [ ] Updated .env with secure database password
- [ ] Set DEBUG=False in .env
- [ ] Configured proper ALLOWED_HOSTS for production domain
- [ ] Set up email credentials for error notifications
- [ ] Verified .env is in .gitignore and not tracked by git

### Database Security
- [ ] Using PostgreSQL (not SQLite) ✅
- [ ] Database credentials are in environment variables
- [ ] Database password is strong (12+ characters, mixed case, numbers, symbols)
- [ ] Database is properly containerized

### Docker & Deployment
- [ ] All hardcoded credentials removed from docker-compose.yml
- [ ] Using docker-compose.production.yml for production
- [ ] Production containers have restart policies
- [ ] SSL certificates configured in nginx.prod.conf
- [ ] Proper volume mounts for persistent data

### Django Security Settings
- [ ] Using settings_production.py for production
- [ ] HTTPS redirects enabled (SECURE_SSL_REDIRECT)
- [ ] Security headers configured
- [ ] CORS properly configured for production domains
- [ ] Static files served securely with WhiteNoise

### Git Security
- [ ] No secrets committed to git history
- [ ] .env file is ignored by git
- [ ] Log files are ignored by git
- [ ] Database files are ignored by git

### Production Environment
- [ ] Environment variables set on hosting platform
- [ ] SSL certificates installed
- [ ] Domain name configured
- [ ] Email delivery tested
- [ ] Error logging configured
- [ ] Monitoring set up

## Security Verification Commands

Run these commands before deployment:

```bash
# Make verification script executable
chmod +x verify-security.sh

# Run security check
./verify-security.sh

# Generate new SECRET_KEY
cd django_project
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Test production configuration locally
docker-compose -f docker-compose.production.yml up --build

# Verify .env is ignored
git check-ignore .env

# Check what files would be committed
git status
```

## Environment Variables for Production

Set these on your hosting platform (Railway, Render, Heroku, etc.):

```
SECRET_KEY=your-generated-secret-key-here
POSTGRES_DB=kapiga_research
POSTGRES_USER=kapiga_user
POSTGRES_PASSWORD=your-secure-production-password
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
ADMIN_EMAIL=admin@your-domain.com
REDIS_URL=redis://redis:6379/0
DATA_RETENTION_DAYS=2555
```

## Post-Deployment Security

### Monitor These Logs:
- `django_project/security_events.log` - Security-related events
- `django_project/security.log` - General security logging
- Container logs for failed authentication attempts

### Regular Security Tasks:
- Monitor error logs for suspicious activity
- Update dependencies regularly
- Review access logs
- Backup database securely
- Test SSL certificate renewal

## Emergency Security Response

If credentials are compromised:

1. **Immediate Actions:**
   - Rotate all passwords and API keys
   - Update SECRET_KEY
   - Check access logs for unauthorized access
   - Monitor for data breaches

2. **Communication:**
   - Notify stakeholders if needed
   - Document the incident
   - Update security procedures

3. **Recovery:**
   - Deploy updated credentials
   - Monitor systems closely
   - Review security policies

---

## ⚠️ CRITICAL REMINDERS

**NEVER commit to git:**
- .env files
- Database files
- Log files with sensitive data
- SSL certificates/private keys
- Backup files
- Files with 'password', 'secret', or 'key' in the name

**Your current .gitignore is excellent and covers these cases!**
