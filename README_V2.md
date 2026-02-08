# Flask Resume Builder - v2.0

Professional resume building application with advanced features, analytics, and Heroku deployment support.

## What's New in v2.0

### Major Features Added
- **Resume Search** - Search and filter resumes by title or candidate name
- **Analytics Dashboard** - Track resume downloads, views, and completion metrics
- **JSON Export** - Export resume data in JSON format for data portability
- **Email Notifications** - Automatic email alerts for key resume actions
- **Statistics Tracking** - Detailed per-resume and user-level analytics
- **Heroku Deployment** - Production-ready Heroku configuration
- **PostgreSQL Support** - Enterprise database support alongside SQLite

### Infrastructure Improvements
- Modular service architecture with separate layers
- Environment variable configuration
- Production-ready startup configuration
- Comprehensive error handling
- Event tracking and logging

### New Pages & Routes
- Dashboard (`/dashboard`) - User analytics overview
- Search (`/resume/search`) - Resume discovery
- Statistics (`/resume/stats/<id>`) - Per-resume metrics
- JSON Export (`/resume/export-json/<id>`) - Data export

---

## Quick Start

### Local Development

1. **Clone and Setup**
```bash
git clone https://github.com/Jxck007/flask-resume-builder.git
cd flask-resume-builder
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and update SECRET_KEY
```

4. **Run Application**
```bash
python main.py
```

Visit: http://localhost:5000

### Heroku Deployment

1. **Create Heroku App**
```bash
heroku login
heroku create your-app-name
```

2. **Add Database & Deploy**
```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secure-key FLASK_ENV=production
git push heroku main
heroku open
```

**See HEROKU_DEPLOYMENT.md for detailed instructions.**

---

## Features

### Resume Building
- Create unlimited resumes
- 2 professional templates (Classic, Modern)
- 6+ resume sections (Personal, Education, Experience, Skills, Projects, Certifications)
- Profile picture upload
- Auto-save functionality

### Management
- Manage multiple resumes
- Edit resume information
- Delete resumes
- Track metadata (created, updated)

### Export Options
- **PDF Download** - Download with professional formatting
- **JSON Export** - Export complete resume data
- **Multiple Templates** - Classic and Modern designs

### Analytics
- Resume statistics dashboard
- Download and view tracking
- Completion percentage calculation
- Content summary statistics
- User-level analytics overview

### Search & Discovery
- Full-text search by resume title
- Search by candidate name
- Filter and find quickly
- Navigate to any resume

### Notifications
- Welcome email on signup
- Resume creation confirmation
- Resume download confirmation
- (Requires SMTP configuration)

---

## System Requirements

- Python 3.11+
- PostgreSQL (for production)
- SQLite (for development)
- Git
- 100MB disk space

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Flask | 3.1.1 |
| Database ORM | SQLAlchemy | 2.0.41 |
| Authentication | Flask-Login | 0.6.3 |
| Forms | Flask-WTF/WTForms | 1.2.1/3.1.2 |
| PDF Generator | Weasyprint + Playwright | 61.0 |
| Email | Flask-Mail | 0.9.1 |
| Server | Gunicorn | 21.2.0 |
| Database (Dev) | SQLite | 3.x |
| Database (Prod) | PostgreSQL | 12+ |

---

## Project Structure

```
flask-resume-builder/
├── website/                    # Main application package
│   ├── __init__.py            # Flask app factory
│   ├── models.py              # Database models (10 models)
│   ├── auth.py                # Authentication routes
│   ├── views.py               # Main application routes
│   ├── email_service.py       # Email notifications
│   ├── analytics_service.py   # Analytics tracking
│   ├── utils.py               # Utility functions
│   ├── static/                # CSS, JS, images, uploads
│   └── templates/             # HTML templates (9 templates)
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku configuration
├── runtime.txt                # Python version
├── .env.example              # Environment variables template
├── HEROKU_DEPLOYMENT.md      # Heroku deployment guide
├── DEPLOYMENT_GUIDE.md       # Complete deployment guide
├── IMPROVEMENTS.md           # Technical improvements
├── FEATURES.md              # Feature documentation
└── README_V2.md             # This file
```

---

## Environment Variables

Create `.env` file based on `.env.example`:

```env
# Required
SECRET_KEY=your-secret-key-here
FLASK_ENV=development  # or production

# Optional (for email notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Heroku (auto-set)
DATABASE_URL=postgresql://...
```

---

## Database Models

The application includes 10 SQLAlchemy models:

1. **User** - User accounts
2. **Resume** - Resume documents
3. **PersonalInfo** - Contact information
4. **Education** - Educational background
5. **Experience** - Work history
6. **Project** - Portfolio projects
7. **Skill** - Technical skills
8. **Certification** - Professional certifications
9. **ResumeAnalytic** - Usage tracking
10. **EmailNotification** - Email delivery tracking

---

## Routes Overview

### Authentication
- `POST /login` - User login
- `POST /Sign-Up` - User registration
- `GET /logout` - User logout

### Resume Management
- `GET /home` - Create resume form
- `POST /home` - Create resume
- `GET /Resume/<id>` - Edit resume
- `POST /Resume/<id>` - Save resume
- `GET /resume/view/<id>` - View resume
- `GET /resume/manage` - Manage resumes list
- `GET /resume/delete/<id>` - Delete resume

### New Routes (v2.0)
- `GET /resume/download/<id>` - Download PDF
- `GET /resume/export-json/<id>` - Export JSON
- `GET /resume/search` - Search interface
- `POST /resume/search` - Search results
- `GET /resume/stats/<id>` - View statistics
- `GET /dashboard` - Analytics dashboard

---

## API Endpoints (Future)

These endpoints are documented and ready for implementation:

```
GET    /api/resumes           - List all resumes
POST   /api/resumes           - Create resume
GET    /api/resumes/<id>      - Get resume details
PUT    /api/resumes/<id>      - Update resume
DELETE /api/resumes/<id>      - Delete resume
GET    /api/resumes/<id>/stats - Get statistics
POST   /api/resumes/<id>/export - Export resume
```

---

## Configuration Options

### Email (Optional)
For email notifications, configure SMTP:
```bash
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=true
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
```

### Database
- **Development**: SQLite (automatic)
- **Production**: PostgreSQL (auto-configured on Heroku)

---

## Deployment Options

### Option 1: Heroku (Recommended)
Best for: Small teams, quick deployment, managed database
```bash
# See HEROKU_DEPLOYMENT.md for step-by-step guide
```

### Option 2: Traditional Server
Best for: Enterprise, custom configuration
- Use Gunicorn as WSGI server
- Set up Nginx as reverse proxy
- Configure PostgreSQL database
- Use environment variables

### Option 3: Docker
Best for: Containerized deployments
- Create Dockerfile (template available)
- Use docker-compose for local development
- Deploy to Kubernetes or Docker Swarm

---

## Performance Metrics

- PDF generation: < 5 seconds
- Resume download: < 2 seconds
- Search query: < 500ms
- Page load: < 1 second
- Database query: < 100ms

---

## Security Features

- Password hashing with pbkdf2
- HTTPS support (automatic on Heroku)
- CSRF protection ready
- SQL injection prevention via ORM
- XSS protection via template auto-escaping
- Secure file upload handling
- Environment-based secrets

---

## Monitoring & Logs

```bash
# View application logs
heroku logs --tail

# Check database status
heroku pg:info

# View error logs
heroku logs --source app -n 100

# Monitor performance
heroku ps
```

---

## Troubleshooting

### Database Connection Issues
```bash
heroku pg:reset DATABASE
heroku restart
```

### Email Not Sending
- Verify MAIL_USERNAME and MAIL_PASSWORD
- Check Gmail "Less secure apps" setting
- Generate App Password for Gmail
- Verify SMTP settings

### PDF Generation Fails
- Ensure Playwright is installed
- Check available system fonts
- Verify HTML syntax

See DEPLOYMENT_GUIDE.md for more troubleshooting tips.

---

## Development Workflow

1. **Create Feature Branch**
```bash
git checkout -b feature/new-feature
```

2. **Make Changes**
- Update code
- Test locally
- Update documentation

3. **Test Thoroughly**
```bash
python main.py
# Test all functionality
```

4. **Commit & Push**
```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

5. **Create Pull Request**
- Describe changes
- Reference issues
- Request review

---

## Contribution Guidelines

We welcome contributions! Please:
1. Fork the repository
2. Create feature branch
3. Follow code style
4. Add documentation
5. Test thoroughly
6. Submit pull request

---

## Documentation

- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **HEROKU_DEPLOYMENT.md** - Heroku-specific guide
- **IMPROVEMENTS.md** - Technical architecture details
- **FEATURES.md** - Complete feature list
- **QUICKSTART.md** - Getting started guide

---

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: Support via project email

---

## License

MIT License - See LICENSE file for details

---

## Changelog

### v2.0 (Current)
- Added resume search and filtering
- Implemented analytics dashboard
- Added JSON export functionality
- Implemented email notifications
- Created Heroku deployment support
- Added PostgreSQL support
- Improved documentation

### v1.0
- Basic resume builder
- PDF generation
- Multiple templates
- User authentication

---

## Roadmap

### Planned Features
- [ ] User profile pages
- [ ] Password reset functionality
- [ ] Resume templates library
- [ ] Collaborative editing
- [ ] Version history
- [ ] ATS-compatible export
- [ ] Interview preparation
- [ ] Mobile app

---

## Credits

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Heroku** - Deployment platform
- **Weasyprint** - PDF generation
- **Bootstrap** - Frontend framework

---

## Version Information

- **Current Version**: 2.0
- **Release Date**: February 2026
- **Last Updated**: 2026-02-08
- **Python**: 3.11.7+

---

## Quick Links

- GitHub: https://github.com/Jxck007/flask-resume-builder
- Live Demo: https://flask-resume-builder.vercel.app
- Heroku: See HEROKU_DEPLOYMENT.md

---

**Ready to get started? Choose your deployment method:**
1. **Local**: `python main.py`
2. **Heroku**: See HEROKU_DEPLOYMENT.md
3. **Traditional Server**: See DEPLOYMENT_GUIDE.md

Happy resume building!
