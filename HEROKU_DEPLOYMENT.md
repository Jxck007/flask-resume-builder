# Heroku Deployment Guide

## Prerequisites

1. Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
2. Git installed and configured
3. Heroku account: https://www.heroku.com

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create Heroku App

```bash
heroku create your-app-name
```

Or let Heroku generate a name:

```bash
heroku create
```

### 3. Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This creates a free PostgreSQL database and sets the `DATABASE_URL` environment variable automatically.

### 4. Set Environment Variables

```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set FLASK_ENV=production
```

For email notifications (optional):

```bash
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=true
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
heroku config:set MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

### 5. Deploy to Heroku

```bash
git push heroku main
```

Or if your branch is `master`:

```bash
git push heroku master
```

### 6. Initialize Database

```bash
heroku run python -c "from website import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 7. Open Your App

```bash
heroku open
```

## View Logs

```bash
heroku logs --tail
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `DATABASE_URL` | PostgreSQL database URL | Auto-set by Heroku |
| `FLASK_ENV` | Set to `production` | Yes |
| `MAIL_SERVER` | SMTP server (e.g., smtp.gmail.com) | No |
| `MAIL_PORT` | SMTP port (e.g., 587) | No |
| `MAIL_USE_TLS` | Use TLS for SMTP | No |
| `MAIL_USERNAME` | SMTP username | No |
| `MAIL_PASSWORD` | SMTP password/app-password | No |
| `MAIL_DEFAULT_SENDER` | Default email sender | No |

## Troubleshooting

### Database Connection Issues

```bash
heroku pg:info
```

### Restart App

```bash
heroku restart
```

### Scale Dynos

```bash
heroku ps:scale web=1
```

### Check Config Variables

```bash
heroku config
```

### Clear Logs

```bash
heroku logs --source app --dyno web -n 100
```

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

## Remove the App

```bash
heroku apps:destroy --app your-app-name
```

## Free Tier Limitations

- Heroku free tier includes:
  - 550 free dyno hours per month (approximately 23 hours per day)
  - One free PostgreSQL database (limited storage)
  - Automatic sleep after 30 minutes of inactivity

For production use, upgrade to a paid plan.

## Gmail SMTP Setup (for Email Notifications)

1. Enable 2-Step Verification on your Google account
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Use the generated 16-character password as `MAIL_PASSWORD`

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure email settings (if needed)
- [ ] Monitor logs regularly
- [ ] Set up backup strategy for database
- [ ] Configure SSL/TLS (automatic on Heroku)
- [ ] Set resource limits if needed
- [ ] Regular database maintenance

## Support

For more information, visit: https://devcenter.heroku.com/articles/getting-started-with-python
