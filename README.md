# SkillMatch Hub 🚀

A comprehensive Career Guidance System built with Django, ensuring students and job seekers find their perfect path through data-driven assessments and community reviews.

## 🌟 Key Features

### 🎯 Interactive Assessment
- **Personality Analysis**: Determines career compatibility based on user traits.
- **Skill Gap Analysis**: Identifies missing skills for desired roles.

### 💼 Career Exploration
- **Detailed Profiles**: In-depth information on salaries, outlook, and requirements.
- **Compatibility Gauge**: A real-time, interactive calculator showing your "Match %" for any job.
- **Review System**: Read and write community reviews with star ratings and helpfulness voting.

### 📊 User Dashboard
- **Saved Careers**: Track jobs you are interested in.
- **Assessment History**: View past results and growth over time.
- **Profile Management**: Customize your professional identity.

## 🛠️ Technology Stack
- **Backend**: Django 6.0 (Python)
- **Frontend**: Tailwind CSS, Alpine.js
- **Database**: SQLite (Dev) / PostgreSQL (Prod)
- **Deployment**: Render / Heroku readiness

## 🚀 Deployment
This project is configured for automated deployment via **Render Blueprints**.
- `render.yaml`: Infrastructure definition.
- `build.sh`: Automated build and migration script.

## 📦 Setup Locally
1. Clone repo
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`
