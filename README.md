# 🔬 Dr. Saidi Kapiga HIV Research Platform

A comprehensive Django-based research portal featuring 30+ years of HIV/AIDS research data, clinical trials analysis, and advanced Python analytics for Dr. Saidi Kapiga's work across Africa.

d ## 🌳 **GitFlow Workflow**

This repository uses GitFlow for organized development. See [GITFLOW.md](./GITFLOW.md) for detailed documentation.

**Quick Start:**
```bash
# Install git-flow
brew install git-flow  # macOS
# or apt-get install git-flow  # Ubuntu

# Initialize GitFlow
./scripts/setup-gitflow.sh

# Start a feature
git flow feature start my-feature
```

## 🚀 **QUICK DEPLOY (30 SECONDS) - RECOMMENDED**

### **Option 1: Railway (FREE + AUTO SSL + ENTERPRISE SECURITY)**

```bash
# 1. Push to GitHub (if not already done)
git add . && git commit -m "Deploy Dr. Kapiga research site" && git push

# 2. Deploy to Railway (literally 30 seconds)
npx @railway/cli login
npx @railway/cli new
# Select "Deploy from GitHub repo" → Your repo → Done!
```

**✅ Includes automatically:**
- Free SSL certificates (Let's Encrypt)
- DDoS protection & Web Application Firewall
- Security headers & HSTS
- PostgreSQL database (managed)
- Redis caching
- Automatic security updates
- SOC2 compliance
- 24/7 monitoring

**💰 Cost: $0/month** (500 execution hours free, then $5/month)

---

## 🛡️ **SECURITY FEATURES INCLUDED**

### **🔒 Your Django App Already Has:**
- ✅ **Force HTTPS** (SECURE_SSL_REDIRECT)
- ✅ **Security Headers** (XSS, CSRF, Clickjacking protection)
- ✅ **Content Security Policy** (CSP) to prevent attacks
- ✅ **Rate Limiting** (100 requests/hour for anonymous users)
- ✅ **Secure Cookies** (HttpOnly, Secure, SameSite)
- ✅ **HSTS** (HTTP Strict Transport Security)
- ✅ **SQL Injection Protection** (Django ORM)
- ✅ **Audit Logging** (Security events logged)

### **🏢 Platform Security (Railway/Render/DO):**
- ✅ **Auto SSL certificates** (A+ rating)
- ✅ **DDoS protection** (enterprise-grade)
- ✅ **Web Application Firewall** (WAF)
- ✅ **Network isolation** (containers)
- ✅ **Compliance** (SOC2, ISO 27001)
- ✅ **Automated security scanning**
- ✅ **Incident response team**

---

## 📋 **ALL DEPLOYMENT OPTIONS**

| Option | Cost | SSL | Security | Setup Time |
|--------|------|-----|----------|------------|
| **Railway** | FREE | ✅ Auto | ⭐⭐⭐⭐⭐ | 30 seconds |
| **Render** | $7/mo | ✅ Auto | ⭐⭐⭐⭐⭐ | 2 minutes |
| **VPS (Vultr)** | $2.50/mo | ⚠️ Script | ⭐⭐⭐⭐ | 30 minutes |
| **DigitalOcean** | $12/mo | ✅ Auto | ⭐⭐⭐⭐⭐ | 5 minutes |

### **🆓 Option 2: Render (FREE tier available)**
```bash
# 1. Connect GitHub repo at render.com
# 2. Select "Web Service" → Connect repo
# 3. Auto-detects Docker → Deploy
```

### **💰 Option 3: VPS with Full Security (Vultr $2.50/month)**
```bash
# 1. Create VPS (512MB, $2.50/month)
ssh root@your-server-ip

# 2. Run automated security setup
git clone https://github.com/your-username/kapiga_research_site
cd kapiga_research_site
chmod +x setup-security.sh
./setup-security.sh your-domain.com admin@your-domain.com

# This automatically sets up:
# ✅ UFW Firewall
# ✅ Fail2ban (intrusion prevention)
# ✅ Let's Encrypt SSL
# ✅ Automated backups
# ✅ System monitoring
# ✅ Security hardening
```

### **🏢 Option 4: DigitalOcean App Platform (Production-ready)**
```bash
# Create app.yaml in your repo:
name: kapiga-research
services:
- name: web
  source_dir: /
  github:
    repo: your-username/kapiga_research_site
    branch: main
  run_command: gunicorn kapiga_site.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
databases:
- name: db
  engine: PG
  size: basic-xs
```

---

## 🚀 Deploying to DigitalOcean App Platform

DigitalOcean App Platform supports Docker Compose for multi-container deployments. Here’s how to deploy your project:

### 1. Push your code to GitHub
Your repo should include `docker-compose.yml`, Dockerfile(s), and `.env.example` (no secrets).

### 2. Create a DigitalOcean account and go to App Platform
- https://cloud.digitalocean.com/apps

### 3. Click "Create App" and connect your GitHub repo
- Select your repository and branch.
- App Platform will auto-detect your `docker-compose.yml` and prompt you to configure each service.

### 4. Configure environment variables
- Use `.env.example` as a reference.
- Set all secrets and production values in the App Platform dashboard (do NOT commit secrets).

### 5. Choose your plan
- Web services require a paid plan after the trial.
- Managed Postgres is recommended for production.

### 6. Deploy
- DigitalOcean will build and run your containers as defined in `docker-compose.yml`.
- Access your app via the provided URL.

### 7. Post-deployment
- Change admin password, configure email, add research data, run analytics, set up custom domain, monitor usage.

---

## 🔍 **VERIFY YOUR SECURITY**

After deployment, check your security rating:

```bash
# Check SSL rating (should be A+)
curl -s "https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com"

# Check security headers
curl -I https://your-domain.com
# Should see: X-Frame-Options, X-Content-Type-Options, etc.

# Verify HTTPS redirect
curl -I http://your-domain.com
# Should see: 301 redirect to HTTPS
```

---

## 📊 **FEATURES INCLUDED**

### **🔬 Research Portal**
- **Homepage**: Research overview and statistics
- **About**: Dr. Kapiga's biography and achievements
- **Studies**: Comprehensive study database with search/filter
- **Publications**: Publication library with citation metrics
- **Analytics**: Interactive charts and research insights
- **Network**: Collaboration network visualization

### **📈 Python Analytics**
- **Jupyter Notebooks**: 3 comprehensive analysis notebooks
  - HIV Research Analysis (publications, citations, impact)
  - Clinical Trials Analysis (FEM-PrEP, Daraja, MEMA kwa Vijana)
  - Geographic & Demographic Analysis (Africa-wide distribution)
- **Django Analytics**: Built-in Python-powered data analysis
- **API Access**: RESTful APIs for data integration

### **🐳 Container Ready**
- **Multi-stage Dockerfile**: Optimized for production
- **Docker Compose**: Full stack with PostgreSQL, Redis, Nginx
- **Health checks**: Application monitoring
- **Volume management**: Persistent data storage

---

## 🗂️ **PROJECT STRUCTURE**

```
kapiga_research_site/
├── 🐍 django_project/          # Django web application
│   ├── kapiga_site/            # Django settings & config
│   ├── research/               # Research data models & views
│   └── templates/              # HTML templates
├── 📊 notebooks/               # Jupyter analysis notebooks
├── 🐳 Dockerfile              # Container configuration
├── 🔧 docker-compose.yml      # Development stack
├── 🔒 docker-compose.production.yml  # Production stack
├── 🛡️ setup-security.sh       # VPS security automation
└── 📋 requirements.txt        # Python dependencies
```

---

## 🔧 **LOCAL DEVELOPMENT**

```bash
# 1. Clone and setup
git clone https://github.com/your-username/kapiga_research_site
cd kapiga_research_site
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Database setup
cd django_project
python manage.py migrate
python manage.py createsuperuser

# 3. Run development server
python manage.py runserver
# Visit: http://localhost:8000

# 4. Run Jupyter notebooks
cd ../notebooks
jupyter lab
# Visit: http://localhost:8888
```

### **🐳 Docker Development**
```bash
# Quick start with Docker
docker-compose up -d
# Visit: http://localhost:8000
# Jupyter: http://localhost:8888
```

---

## 📱 **ACCESS YOUR DEPLOYED SITE**

After deployment:
- **🌐 Research Portal**: `https://your-app-name.railway.app` (or your domain)
- **🔧 Admin Panel**: `https://your-app-name.railway.app/admin`
- **📊 API Documentation**: `https://your-app-name.railway.app/api`
- **📈 Analytics**: `https://your-app-name.railway.app/analytics`

---

## 📚 **RESEARCH DATA INCLUDED**

Based on Dr. Saidi Kapiga's actual research:

### **🔬 Major Studies**
- **FEM-PrEP Trial**: Pre-exposure prophylaxis for African women (2,120 participants)
- **Daraja Trial**: Social worker intervention for HIV patients (500 participants)
- **MEMA kwa Vijana**: Adolescent health intervention (13,500 participants)
- **DoRIS HPV Study**: Single-dose HPV vaccination (930 participants)

### **🌍 Geographic Coverage**
- **5 African Countries**: Tanzania, Kenya, Uganda, South Africa, Malawi
- **20+ Research Sites**: From Mwanza to Cape Town
- **50,000+ Participants**: Across all studies
- **30+ Years**: Research timeline (1995-2025)

### **📊 Analytics Capabilities**
- Publication trend analysis
- Citation network mapping
- Geographic research distribution
- Demographic analysis
- Collaboration network visualization
- Clinical trial outcome analysis

---

## 🎯 **NEXT STEPS AFTER DEPLOYMENT**

1. **🔑 Change Admin Password**: Login to `/admin` and update credentials
2. **📧 Configure Email**: Update email settings in environment variables
3. **🗃️ Add Research Data**: Use admin panel to add studies and publications
4. **📈 Run Analytics**: Execute Jupyter notebooks for insights
5. **🌐 Custom Domain**: Point your domain to the deployed app
6. **📊 Monitor Usage**: Check analytics and performance

---

## 💡 **SUPPORT & DOCUMENTATION**

- **🐛 Issues**: Create GitHub issues for bugs
- **📖 Django Docs**: https://docs.djangoproject.com/
- **🐳 Docker Docs**: https://docs.docker.com/
- **🚀 Railway Docs**: https://docs.railway.app/
- **🔒 Security Guide**: See `SECURITY.md`

---

## 🏆 **RECOMMENDED DEPLOYMENT PATH**

### **Phase 1: Start Free (0-3 months)**
✅ **Railway FREE tier** - Validate application, gather users

### **Phase 2: Scale Affordably (3-12 months)**
💰 **Vultr VPS ($2.50/month)** - Cost-effective scaling

### **Phase 3: Production Ready (12+ months)**
🏢 **DigitalOcean App Platform ($12/month)** - Enterprise features

---

## 🎉 **YOU'RE ALL SET!**

Your Dr. Saidi Kapiga HIV Research Platform is ready to deploy with:
- ✅ **Enterprise-grade security** (SSL, DDoS protection, WAF)
- ✅ **Professional design** (responsive, accessible)
- ✅ **Advanced analytics** (Python, Jupyter, visualizations)
- ✅ **Scalable architecture** (containerized, cloud-ready)
- ✅ **Research compliance** (data protection, audit logs)

**Deploy now in 30 seconds with Railway, or choose your preferred platform!** 🚀
