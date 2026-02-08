from .models import db, ResumeAnalytic
from datetime import datetime

def track_event(user_id, resume_id, action, details=None):
    try:
        analytic = ResumeAnalytic(
            user_id=user_id,
            resume_id=resume_id,
            action=action,
            details=details
        )
        db.session.add(analytic)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error tracking event: {e}")
        return False

def get_user_analytics(user_id):
    analytics = ResumeAnalytic.query.filter_by(user_id=user_id).all()
    return analytics

def get_resume_analytics(resume_id):
    analytics = ResumeAnalytic.query.filter_by(resume_id=resume_id).all()
    return analytics

def get_resume_stats(resume_id):
    from .models import Resume
    resume = Resume.query.get(resume_id)

    if not resume:
        return None

    downloads = ResumeAnalytic.query.filter_by(
        resume_id=resume_id,
        action='download'
    ).count()

    views = ResumeAnalytic.query.filter_by(
        resume_id=resume_id,
        action='view'
    ).count()

    return {
        'resume_id': resume_id,
        'title': resume.title,
        'downloads': downloads,
        'views': views,
        'created_at': resume.created_at,
        'updated_at': resume.updated_at
    }

def get_all_user_stats(user_id):
    from .models import Resume
    resumes = Resume.query.filter_by(user_id=user_id).all()

    stats = []
    for resume in resumes:
        stats.append(get_resume_stats(resume.id))

    return stats
