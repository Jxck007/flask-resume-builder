web: gunicorn main:app
release: python -c "from website import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
