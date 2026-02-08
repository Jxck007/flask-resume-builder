from flask import Flask, render_template_string
from flask_mail import Mail, Message
from datetime import datetime
from .models import db, EmailNotification
import os

mail = Mail()

def init_email(app):
    mail.init_app(app)

def send_email_async(subject, recipients, text_body=None, html_body=None, user_id=None):
    try:
        msg = Message(subject, recipients=recipients)
        if text_body:
            msg.body = text_body
        if html_body:
            msg.html = html_body

        mail.send(msg)

        if user_id:
            notification = EmailNotification(
                user_id=user_id,
                subject=subject,
                body=text_body or html_body,
                is_sent=True
            )
            db.session.add(notification)
            db.session.commit()

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        if user_id:
            notification = EmailNotification(
                user_id=user_id,
                subject=subject,
                body=text_body or html_body,
                is_sent=False
            )
            db.session.add(notification)
            db.session.commit()
        return False

def send_welcome_email(user_email, username):
    subject = "Welcome to Resume Builder"
    html_body = f"""
    <h2>Welcome, {username}!</h2>
    <p>Thank you for creating an account with Resume Builder.</p>
    <p>Start building your professional resume today and download it as PDF.</p>
    <p>Features include:</p>
    <ul>
        <li>Multiple professional templates</li>
        <li>Easy-to-use form interface</li>
        <li>PDF export capability</li>
        <li>Manage multiple resumes</li>
    </ul>
    <p>Happy resume building!</p>
    """
    send_email_async(subject, [user_email], html_body=html_body)

def send_resume_created_email(user_email, resume_title):
    subject = f"Resume '{resume_title}' Created Successfully"
    html_body = f"""
    <h2>Resume Created!</h2>
    <p>Your resume "<strong>{resume_title}</strong>" has been created successfully.</p>
    <p>You can now:</p>
    <ul>
        <li>Add your personal information</li>
        <li>Add education details</li>
        <li>Add work experience</li>
        <li>Add projects and skills</li>
        <li>Download as PDF</li>
    </ul>
    <p>Visit your dashboard to continue editing.</p>
    """
    send_email_async(subject, [user_email], html_body=html_body)

def send_resume_downloaded_email(user_email, resume_title):
    subject = f"Resume '{resume_title}' Downloaded"
    html_body = f"""
    <h2>Download Confirmation</h2>
    <p>Your resume "<strong>{resume_title}</strong>" has been downloaded successfully.</p>
    <p>Thank you for using Resume Builder!</p>
    """
    send_email_async(subject, [user_email], html_body=html_body)
