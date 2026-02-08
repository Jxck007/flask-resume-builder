import json
from datetime import datetime
from .models import Resume, PersonalInfo, Education, Experience, Project, Skill, Certification

def serialize_resume_to_dict(resume):
    """Convert resume to dictionary for JSON export"""
    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()

    resume_dict = {
        'id': resume.id,
        'title': resume.title,
        'style': resume.style,
        'created_at': resume.created_at.isoformat() if resume.created_at else None,
        'updated_at': resume.updated_at.isoformat() if resume.updated_at else None,
    }

    if info:
        resume_dict['personal_info'] = {
            'full_name': info.full_name,
            'phone': info.phone,
            'email': info.resume_email,
            'linkedin': info.linkedin,
            'github': info.github,
            'address': info.address,
            'summary': info.summary
        }

    educations = Education.query.filter_by(resume_id=resume.id).all()
    resume_dict['education'] = [
        {
            'degree': edu.degree,
            'institution': edu.institution,
            'start_year': edu.start_year,
            'end_year': edu.end_year,
            'cgpa': edu.cgpa,
            'description': edu.description
        } for edu in educations
    ]

    experiences = Experience.query.filter_by(resume_id=resume.id).all()
    resume_dict['experience'] = [
        {
            'job_title': exp.job_title,
            'company': exp.company,
            'start_date': exp.start_date,
            'end_date': exp.end_date,
            'description': exp.description
        } for exp in experiences
    ]

    projects = Project.query.filter_by(resume_id=resume.id).all()
    resume_dict['projects'] = [
        {
            'title': proj.title,
            'description': proj.description,
            'tech_stack': proj.tech_stack,
            'link': proj.link
        } for proj in projects
    ]

    skills = Skill.query.filter_by(resume_id=resume.id).all()
    resume_dict['skills'] = [
        {
            'name': skill.name,
            'level': skill.level
        } for skill in skills
    ]

    certifications = Certification.query.filter_by(resume_id=resume.id).all()
    resume_dict['certifications'] = [
        {
            'name': cert.name,
            'issuer': cert.issuer,
            'issue_date': cert.issue_date,
            'credential_link': cert.credential_link
        } for cert in certifications
    ]

    return resume_dict

def export_resume_json(resume):
    """Export resume as JSON string"""
    resume_dict = serialize_resume_to_dict(resume)
    return json.dumps(resume_dict, indent=2)

def search_resumes(user_id, query):
    """Search resumes by title and personal info"""
    from . import db

    resumes = Resume.query.filter_by(user_id=user_id).all()
    results = []

    for resume in resumes:
        if query.lower() in resume.title.lower():
            results.append(resume)
            continue

        info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
        if info and query.lower() in info.full_name.lower():
            results.append(resume)

    return results

def get_resume_statistics(resume):
    """Get statistics about resume completion"""
    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    education_count = Education.query.filter_by(resume_id=resume.id).count()
    experience_count = Experience.query.filter_by(resume_id=resume.id).count()
    project_count = Project.query.filter_by(resume_id=resume.id).count()
    skill_count = Skill.query.filter_by(resume_id=resume.id).count()
    cert_count = Certification.query.filter_by(resume_id=resume.id).count()

    completion_items = [
        bool(info),
        bool(education_count > 0),
        bool(experience_count > 0),
        bool(project_count > 0),
        bool(skill_count > 0),
        bool(cert_count > 0)
    ]

    completion_percentage = (sum(completion_items) / len(completion_items)) * 100

    return {
        'personal_info': bool(info),
        'education_count': education_count,
        'experience_count': experience_count,
        'project_count': project_count,
        'skill_count': skill_count,
        'certification_count': cert_count,
        'completion_percentage': round(completion_percentage, 2)
    }
