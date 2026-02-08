# Flask Resume Builder - Complete Deployment Guide

## Quick Start

### Local Development Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Create .env File**
```bash
cp .env.example .env
# Edit .env and update SECRET_KEY
```

4. **Run Application**
```bash
python main.py
```

Visit: `http://localhost:5000`

---

## Heroku Deployment (Recommended)

### Prerequisites
- Heroku CLI installed
- Git configured
- Heroku account

### Step-by-Step Deployment

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku App**
```bash
heroku create your-app-name
# Or let Heroku generate: heroku create
```

3. **Add PostgreSQL Database** (automatically sets DATABASE_URL)
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY=your-secure-secret-key
heroku config:set FLASK_ENV=production
```

5. **Deploy Code**
```bash
git push heroku main
# Or: git push heroku master (if your branch is master)
```

6. **View Logs**
```bash
heroku logs --tail
```

7. **Open Application**
```bash
heroku open
```

---

## New Features Implemented

### 1. Resume Search
- Search resumes by title and personal name
- Filter results instantly
- Located at: `/resume/search`

### 2. Analytics & Statistics
- Track resume downloads and views
- View completion percentage
- Content summary statistics
- Access via: `/resume/stats/<resume_id>`
- Dashboard: `/dashboard`

### 3. JSON Export
- Export entire resume as JSON format
- Preserves all resume data
- Easy data portability
- Button in manage page

### 4. Email Notifications
- Welcome emails on account creation
- Resume download confirmations
- Requires SMTP configuration
- See email setup section below

### 5. Improved Database
- Added SQLAlchemy models for analytics
- Email notification tracking
- Resume metadata tracking
- Timestamps for all actions

### 6. Responsive UI
- New dashboard page with metrics
- Search interface
- Statistics page with completion tracking
- Mobile-friendly design

---

## Email Setup (Optional)

### Gmail SMTP Configuration

1. **Enable 2-Step Verification** on your Google account
2. **Generate App Password**: https://myaccount.google.com/apppasswords
3. **Set Heroku Config Variables**
```bash
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=true
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-16-char-app-password
heroku config:set MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Alternative: SendGrid

```bash
heroku config:set MAIL_SERVER=smtp.sendgrid.net
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=true
heroku config:set MAIL_USERNAME=apikey
heroku config:set MAIL_PASSWORD=your-sendgrid-api-key
```

---

## Project Structure

```
flask-resume-builder/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── Procfile                     # Heroku configuration
├── runtime.txt                  # Python version
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── website/
│   ├── __init__.py             # Flask app factory
│   ├── models.py               # Database models (8 models)
│   ├── auth.py                 # Authentication routes
│   ├── views.py                # Main application routes
│   ├── email_service.py        # Email notification handler
│   ├── analytics_service.py    # Analytics tracking
│   ├── utils.py                # Utility functions
│   ├── static/
│   │   ├── css/
│   │   │   ├── classic.css     # Classic template
│   │   │   └── modern.css      # Modern template
│   │   ├── js/
│   │   ├── uploads/            # Profile pictures
│   │   └── templates_image/
│   └── templates/
│       ├── base.html           # Base template
│       ├── login.html          # Login page
│       ├── signup.html         # Registration page
│       ├── home.html           # Home/create resume
│       ├── resumetemplate.html # Resume editor
│       ├── resume_base.html    # Resume preview
│       ├── manage.html         # Manage resumes
│       ├── search.html         # Search interface
│       ├── stats.html          # Statistics page
│       └── dashboard.html      # User dashboard
└── HEROKU_DEPLOYMENT.md        # Detailed Heroku guide
```

---

## Database Models

The application includes 8 SQLAlchemy models:

1. **User** - User accounts and authentication
2. **Resume** - Resume documents with metadata
3. **PersonalInfo** - Contact and profile information
4. **Education** - Educational background
5. **Experience** - Work history
6. **Project** - Projects and portfolio items
7. **Skill** - Technical and soft skills
8. **Certification** - Professional certifications
9. **ResumeAnalytic** - Usage tracking and analytics
10. **EmailNotification** - Email delivery tracking

---

## Environment Variables Reference

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| SECRET_KEY | Flask session security | Yes | None |
| FLASK_ENV | Environment mode | Yes | development |
| DATABASE_URL | Database connection | No (SQLite for dev) | sqlite:///ResumeBuilder.db |
| MAIL_SERVER | SMTP server | No | smtp.gmail.com |
| MAIL_PORT | SMTP port | No | 587 |
| MAIL_USE_TLS | Use TLS encryption | No | true |
| MAIL_USERNAME | SMTP username | No | None |
| MAIL_PASSWORD | SMTP password | No | None |
| MAIL_DEFAULT_SENDER | Default sender email | No | noreply@resumebuilder.com |
| PORT | Server port | No | 5000 |

---

## Deployment Checklist

### Before Deploying

- [ ] Update SECRET_KEY to a strong random value
- [ ] Set FLASK_ENV=production
- [ ] Test locally with `python main.py`
- [ ] Commit all changes to Git
- [ ] Create `.env` file (not committed)
- [ ] Test PDF generation locally
- [ ] Verify database connection

### Heroku Deployment

- [ ] Install Heroku CLI
- [ ] Run `heroku login`
- [ ] Create app: `heroku create your-app-name`
- [ ] Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
- [ ] Set environment variables
- [ ] Deploy: `git push heroku main`
- [ ] Monitor logs: `heroku logs --tail`
- [ ] Test app functionality

### Post-Deployment

- [ ] Verify database created: `heroku run "python -c 'from website import create_app, db; app = create_app(); print(\"Database OK\")'"`
- [ ] Test login functionality
- [ ] Create test resume
- [ ] Test PDF download
- [ ] Check email notifications (if configured)
- [ ] Monitor error logs
- [ ] Set up monitoring/alerts

---

## Troubleshooting

### Database Issues

**Error: "No such table"**
```bash
heroku run "python -c \"from website import create_app, db; app = create_app(); app.app_context().push(); db.create_all()\""
```

**Check Database Status**
```bash
heroku pg:info
```

### Dyno Issues

**App Won't Start**
```bash
heroku logs --tail
heroku ps
```

**Scale Dynos**
```bash
heroku ps:scale web=1
```

### Reset Database

**Warning: This deletes all data!**
```bash
heroku pg:reset DATABASE
heroku restart
```

---

## Performance Optimization

1. **Enable Caching**
   - Cache PDF generation
   - Cache user resumes list

2. **Database Optimization**
   - Add indexes on frequently queried columns
   - Optimize query joins

3. **Frontend Optimization**
   - Minify CSS/JS
   - Lazy load images
   - Use CDN for static files

4. **Heroku Optimization**
   - Use production-tier PostgreSQL
   - Enable New Relic monitoring
   - Configure auto-scaling

---

## Security Best Practices

1. **Never commit .env file**
   - Use `.env.example` as template
   - All secrets in Heroku config

2. **Use HTTPS** (automatic on Heroku)
   - Force HTTPS redirect
   - Set secure cookies

3. **SQL Injection Prevention**
   - Use SQLAlchemy ORM (implemented)
   - Never use raw SQL for user input

4. **XSS Protection**
   - Jinja2 auto-escapes (implemented)
   - Validate all file uploads

5. **CSRF Protection**
   - Flask-WTF CSRF tokens (consider adding)
   - Session validation

6. **Password Security**
   - Use werkzeug.security for hashing (implemented)
   - Minimum 7 characters with mixed case

---

## Monitoring & Logs

### View Logs
```bash
heroku logs --tail                    # Real-time logs
heroku logs -n 100                    # Last 100 lines
heroku logs --source app              # App logs only
heroku logs --source heroku           # Heroku system logs
```

### Performance Monitoring

Add free monitoring with New Relic:
```bash
heroku addons:create newrelic:wayne
```

---

## Backup & Maintenance

### Database Backup
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

### Scheduled Tasks

For background jobs, consider:
- Heroku Scheduler (free)
- Clock processes
- Queue workers (paid)

---

## Upgrade Path

### Add More Features
1. User profiles and avatars
2. Resume templates library
3. Interview preparation tools
4. Job application tracking
5. Resume sharing and public profiles
6. Collaboration features

### Scale Infrastructure
1. Migrate to production PostgreSQL tier
2. Add Redis for caching
3. Implement CDN for static files
4. Add background worker dyos
5. Set up monitoring alerts

---

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Heroku Docs**: https://devcenter.heroku.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/

---

## License

This project is provided as-is for educational and commercial use.

---

## Version History

### v2.0 (Current)
- Added search and filtering
- Implemented analytics tracking
- Added JSON export functionality
- Email notification support
- Heroku deployment ready
- Enhanced UI with dashboard

### v1.0
- Basic resume builder
- PDF generation
- Multiple templates
- User authentication
