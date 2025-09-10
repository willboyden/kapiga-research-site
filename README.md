# Kapiga Research Site

This repository contains the Django/Postgres research analytics site for Dr. Saidi Kapiga. It includes Docker setup, Jupyter notebooks, and a research analytics dashboard.

## Features
- Django 4.2.7 web application
- Postgres database
- Docker Compose for easy setup
- Jupyter notebooks for research analysis
- Analytics dashboard with metrics and visualizations

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/willboyden/kapiga-research-site.git
   cd kapiga-research-site
   ```

2. **Create a `.env` file:**
   Copy `.env.example` to `.env` and fill in your secrets (do NOT commit `.env`):
   ```bash
   cp .env.example .env
   # Edit .env and set DATABASE_URL, SECRET_KEY, etc.
   ```

3. **Build and start Docker containers:**
   ```bash
   docker-compose build
   docker-compose up
   ```

4. **Apply migrations and load data:**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py loaddata /app/data/kapiga_fixture.json
   ```

5. **Access the site:**
   - Web: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Security Notes
- **Never commit your `.env` file or any secrets.**
- The repository does NOT include any passwords, secrets, or sensitive data.
- All credentials and secrets should be kept in `.env` (which is in `.gitignore`).

## Development
- Python 3.11 recommended
- Django 4.2.7
- Postgres 14+
- See `requirements.txt` for dependencies

## Folder Structure
- `django_project/` - Django app and settings
- `data/` - Example data and analysis results
- `notebooks/` - Jupyter notebooks for research
- `docker-compose.yml` - Docker Compose config
- `Dockerfile` - Web app Dockerfile

## License
MIT (see LICENSE)

---
For questions, contact William Boyden (willboyden@github.com)
