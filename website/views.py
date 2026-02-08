from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import *
from .analytics_service import track_event
from .utils import export_resume_json, search_resumes, get_resume_statistics
import os
import asyncio
import shutil
import time
import uuid
from playwright.async_api import async_playwright
from datetime import datetime

views = Blueprint('views', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        resume_email = request.form.get('resume_email')
        phone = request.form.get('phone')
        github = request.form.get('github')
        linkedin = request.form.get('linkedin')
        summary = request.form.get('summary')
        style = request.form.get('template')
        profile_pic = request.files.get('profile_pic')

        if not full_name or not resume_email:
            flash("Full Name and Resume Email are required.", "danger")
            return redirect(url_for('views.home'))

        filename = 'default.jpg'
        if profile_pic and profile_pic.filename != '':
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Generate unique filename with timestamp for cache busting
                ext = os.path.splitext(profile_pic.filename)[1]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                filename = f"profile_new_{timestamp}_{unique_id}{ext}"
                filename = secure_filename(filename)
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                profile_pic.save(filepath)
            except Exception as e:
                flash(f"Error uploading image: {str(e)}", "danger")
                print(f"Image upload error: {e}")
                filename = 'default.jpg'

        resume = Resume(user_id=current_user.id, title=f"{full_name}'s Resume", style=style)
        db.session.add(resume)
        db.session.commit()

        info = PersonalInfo(
            resume_id=resume.id,
            full_name=full_name,
            resume_email=resume_email,
            phone=phone,
            github=github,
            linkedin=linkedin,
            summary=summary,
            profile_pic=filename
        )
        db.session.add(info)
        db.session.commit()

        flash("Basic resume info saved! Now complete your resume.", "success")
        return redirect(url_for('views.create_resume', resume_id=resume.id))

    return render_template("home.html")

@views.route('/Resume/<int:resume_id>', methods=['GET', 'POST'])
@login_required
def create_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.home'))

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    educations = Education.query.filter_by(resume_id=resume.id).all()
    experiences = Experience.query.filter_by(resume_id=resume.id).all()
    projects = Project.query.filter_by(resume_id=resume.id).all()
    skills = Skill.query.filter_by(resume_id=resume.id).all()
    certifications = Certification.query.filter_by(resume_id=resume.id).all()

    if request.method == 'POST':
        # Update personal info
        info.full_name = request.form.get('full_name')
        info.resume_email = request.form.get('resume_email')
        info.phone = request.form.get('phone')
        info.github = request.form.get('github')
        info.linkedin = request.form.get('linkedin')
        info.summary = request.form.get('summary')

        # Handle profile picture - with proper cleanup and cache busting
        profile_pic = request.files.get('profile_pic')
        if profile_pic and profile_pic.filename != '':
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Delete old image file completely if it exists
                if info.profile_pic and info.profile_pic != 'default.jpg':
                    old_path = os.path.join(UPLOAD_FOLDER, info.profile_pic)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                            time.sleep(0.1)  # Small delay to ensure file is freed
                        except Exception as e:
                            print(f"Warning: Could not delete old image: {e}")
                
                # Generate unique filename with timestamp to prevent caching issues
                ext = os.path.splitext(profile_pic.filename)[1]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                filename = f"profile_{current_user.id}_{timestamp}_{unique_id}{ext}"
                filename = secure_filename(filename)
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                profile_pic.save(filepath)
                
                # Update database with new filename
                info.profile_pic = filename
            except Exception as e:
                flash(f"Error uploading image: {str(e)}", "danger")
                print(f"Image upload error: {e}")

        # Update education
        edu_degree = request.form.getlist('degree[]')
        edu_institution = request.form.getlist('institution[]')
        edu_start = request.form.getlist('start_year[]')
        edu_end = request.form.getlist('end_year[]')
        edu_desc = request.form.getlist('edu_description[]')
        
        # Delete old educations and create new ones
        Education.query.filter_by(resume_id=resume.id).delete()
        for i, degree in enumerate(edu_degree):
            if degree.strip():  # Only save if not empty
                edu = Education(
                    resume_id=resume.id,
                    degree=degree,
                    institution=edu_institution[i] if i < len(edu_institution) else '',
                    start_year=edu_start[i] if i < len(edu_start) else '',
                    end_year=edu_end[i] if i < len(edu_end) else '',
                    description=edu_desc[i] if i < len(edu_desc) else ''
                )
                db.session.add(edu)

        # Update experience
        exp_title = request.form.getlist('job_title[]')
        exp_company = request.form.getlist('company[]')
        exp_start = request.form.getlist('start_date[]')
        exp_end = request.form.getlist('end_date[]')
        exp_desc = request.form.getlist('exp_description[]')
        
        Experience.query.filter_by(resume_id=resume.id).delete()
        for i, title in enumerate(exp_title):
            if title.strip():
                exp = Experience(
                    resume_id=resume.id,
                    job_title=title,
                    company=exp_company[i] if i < len(exp_company) else '',
                    start_date=exp_start[i] if i < len(exp_start) else '',
                    end_date=exp_end[i] if i < len(exp_end) else '',
                    description=exp_desc[i] if i < len(exp_desc) else ''
                )
                db.session.add(exp)

        # Update projects
        proj_title = request.form.getlist('project_title[]')
        proj_desc = request.form.getlist('project_description[]')
        proj_tech = request.form.getlist('tech_stack[]')
        proj_link = request.form.getlist('project_link[]')
        
        Project.query.filter_by(resume_id=resume.id).delete()
        for i, title in enumerate(proj_title):
            if title.strip():
                proj = Project(
                    resume_id=resume.id,
                    title=title,
                    description=proj_desc[i] if i < len(proj_desc) else '',
                    tech_stack=proj_tech[i] if i < len(proj_tech) else '',
                    link=proj_link[i] if i < len(proj_link) else ''
                )
                db.session.add(proj)

        # Update skills
        skill_names = request.form.getlist('skill_name[]')
        skill_levels = request.form.getlist('skill_level[]')
        
        Skill.query.filter_by(resume_id=resume.id).delete()
        for i, name in enumerate(skill_names):
            if name.strip():
                skill = Skill(
                    resume_id=resume.id,
                    name=name,
                    level=skill_levels[i] if i < len(skill_levels) else 'intermediate'
                )
                db.session.add(skill)

        # Update certifications
        cert_names = request.form.getlist('cert_name[]')
        cert_issuers = request.form.getlist('issuer[]')
        cert_dates = request.form.getlist('issue_date[]')
        cert_links = request.form.getlist('credential_link[]')
        
        Certification.query.filter_by(resume_id=resume.id).delete()
        for i, name in enumerate(cert_names):
            if name.strip():
                cert = Certification(
                    resume_id=resume.id,
                    name=name,
                    issuer=cert_issuers[i] if i < len(cert_issuers) else '',
                    issue_date=cert_dates[i] if i < len(cert_dates) else '',
                    credential_link=cert_links[i] if i < len(cert_links) else ''
                )
                db.session.add(cert)

        db.session.add(info)
        db.session.commit()

        flash("Resume updated successfully!", "success")
        return redirect(url_for('views.view_resume', resume_id=resume.id))

    return render_template("resumetemplate.html", Resume=resume, PersonalInfo=info, 
                           educations=educations, experiences=experiences, projects=projects,
                           skills=skills, certifications=certifications)

@views.route('/resume/view/<int:resume_id>')
@login_required
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("You are not authorized to view this resume.", "danger")
        return redirect(url_for('views.home'))

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    educations = Education.query.filter_by(resume_id=resume.id).all()
    experiences = Experience.query.filter_by(resume_id=resume.id).all()
    projects = Project.query.filter_by(resume_id=resume.id).all()
    skills = Skill.query.filter_by(resume_id=resume.id).all()
    certifications = Certification.query.filter_by(resume_id=resume.id).all()

    return render_template("resume_base.html", resume=resume, info=info, 
                           educations=educations, experiences=experiences, 
                           projects=projects, skills=skills, certifications=certifications)

@views.route('/resume/manage')
@login_required
def manage_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template("manage.html", resumes=resumes)

@views.route('/resume/delete/<int:resume_id>')
@login_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))
    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    if info and info.profile_pic and info.profile_pic != 'default.jpg':
        img_path = os.path.join(UPLOAD_FOLDER, info.profile_pic)
        if os.path.exists(img_path):
            os.remove(img_path)
    PersonalInfo.query.filter_by(resume_id=resume.id).delete()
    Education.query.filter_by(resume_id=resume.id).delete()
    Experience.query.filter_by(resume_id=resume.id).delete()
    Project.query.filter_by(resume_id=resume.id).delete()
    Skill.query.filter_by(resume_id=resume.id).delete()
    Certification.query.filter_by(resume_id=resume.id).delete()

    db.session.delete(resume)
    db.session.commit()

    flash("Resume and image deleted successfully.", "success")
    return redirect(url_for('views.manage_resumes'))
@views.route('/resume/download/<int:resume_id>')
@login_required
def download_resume(resume_id):
    """Download resume as PDF with improved error handling and async management"""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))

    track_event(current_user.id, resume_id, 'download', f'Downloaded resume: {resume.title}')
    resume.download_count += 1
    db.session.commit()

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    if not info:
        flash("Resume information not found.", "danger")
        return redirect(url_for('views.manage_resumes'))

    educations = Education.query.filter_by(resume_id=resume.id).all()
    experiences = Experience.query.filter_by(resume_id=resume.id).all()
    projects = Project.query.filter_by(resume_id=resume.id).all()
    skills = Skill.query.filter_by(resume_id=resume.id).all()
    certifications = Certification.query.filter_by(resume_id=resume.id).all()

    # Create unique temporary paths
    temp_id = str(uuid.uuid4())[:8]
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    # Verify image exists
    image_path = os.path.join(static_folder, 'uploads', info.profile_pic or 'default.jpg')
    if not os.path.exists(image_path):
        image_path = os.path.join(static_folder, 'uploads', 'default.jpg')
    
    css_path = os.path.join(static_folder, 'css', f"{resume.style}.css")
    if not os.path.exists(css_path):
        flash("Resume style not found.", "danger")
        return redirect(url_for('views.manage_resumes'))

    # Temporary files with unique IDs
    html_path = os.path.join(static_folder, f"resume_{resume_id}_{temp_id}.html")
    pdf_path = os.path.join(static_folder, f"resume_{resume_id}_{temp_id}.pdf")

    try:
        # Render HTML template
        html_content = render_template(
            "resume_base.html", 
            resume=resume, 
            info=info,
            educations=educations, 
            experiences=experiences,
            projects=projects, 
            skills=skills, 
            certifications=certifications,
            is_download=True,
            static_image_path=image_path,
            css_path=css_path
        )

        # Write HTML to temporary file
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generate PDF asynchronously with proper error handling
        try:
            asyncio.run(_generate_pdf_async(html_path, pdf_path))
        except Exception as async_error:
            print(f"Async PDF generation error: {async_error}")
            raise Exception(f"PDF generation failed: {str(async_error)}")

        # Verify PDF was created
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
            raise Exception("PDF file was not generated properly")

        # Prepare file for download with safe filename
        safe_title = "".join(c for c in resume.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        download_name = f"{safe_title}.pdf"

        # Send file to user
        return send_file(
            pdf_path, 
            as_attachment=True, 
            download_name=download_name,
            mimetype='application/pdf'
        )

    except Exception as e:
        error_msg = f"PDF generation failed: {str(e)}"
        print(f"Download error: {error_msg}")
        flash(error_msg, "danger")
        return redirect(url_for('views.manage_resumes'))

    finally:
        # Clean up temporary files (best effort)
        for temp_file in [html_path, pdf_path]:
            try:
                if os.path.exists(temp_file):
                    # Delay before deletion to ensure file is released
                    time.sleep(0.2)
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not clean up {temp_file}: {e}")


@views.route('/resume/export-json/<int:resume_id>')
@login_required
def export_resume_json_route(resume_id):
    """Export resume as JSON file"""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))

    try:
        json_data = export_resume_json(resume)
        track_event(current_user.id, resume_id, 'export', f'Exported resume as JSON: {resume.title}')

        return send_file(
            path_or_file=__import__('io').BytesIO(json_data.encode()),
            as_attachment=True,
            download_name=f"{resume.title.replace(' ', '_')}.json",
            mimetype='application/json'
        )
    except Exception as e:
        flash(f"Error exporting resume: {str(e)}", "danger")
        return redirect(url_for('views.manage_resumes'))

@views.route('/resume/search', methods=['GET', 'POST'])
@login_required
def search_resume():
    """Search resumes by title or name"""
    results = []
    query = request.args.get('q', '') if request.method == 'GET' else request.form.get('search_query', '')

    if query:
        results = search_resumes(current_user.id, query)

    return render_template("search.html", results=results, query=query)

@views.route('/resume/stats/<int:resume_id>')
@login_required
def resume_stats(resume_id):
    """Get resume statistics"""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))

    stats = get_resume_statistics(resume)
    return render_template("stats.html", resume=resume, stats=stats)

@views.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with analytics"""
    from .analytics_service import get_all_user_stats

    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    all_stats = get_all_user_stats(current_user.id)

    total_downloads = sum(stat['downloads'] for stat in all_stats if stat)
    total_views = sum(stat['views'] for stat in all_stats if stat)

    return render_template("dashboard.html", resumes=resumes, stats=all_stats,
                         total_downloads=total_downloads, total_views=total_views)

async def _generate_pdf_async(html_path, pdf_path):
    """Generate PDF from HTML using Playwright with proper cleanup"""
    browser = None
    try:
        # Launch browser with explicit timeout
        async with async_playwright() as p:
            # Use chromium with explicit args for better stability
            browser = await p.chromium.launch(
                args=['--disable-blink-features=AutomationControlled']
            )

            try:
                context = await browser.new_context()
                page = await context.new_page()

                # Load HTML file with proper error handling
                file_url = f"file:///{html_path.replace(os.sep, '/')}"

                try:
                    # Navigate to page with timeout
                    await page.goto(file_url, wait_until="networkidle", timeout=30000)
                except Exception as nav_error:
                    print(f"Navigation error: {nav_error}")
                    # Try without networkidle
                    await page.goto(file_url, wait_until="load", timeout=30000)

                # Generate PDF with proper settings
                await page.pdf(
                    path=pdf_path,
                    format="A4",
                    print_background=True,
                    margin={
                        'top': '0.5in',
                        'bottom': '0.5in',
                        'left': '0.5in',
                        'right': '0.5in'
                    }
                )

                await context.close()
                print(f"PDF generated successfully: {pdf_path}")

            except Exception as context_error:
                print(f"Context error: {context_error}")
                raise
            finally:
                if browser:
                    await browser.close()

    except Exception as e:
        print(f"Playwright error: {e}")
        raise
