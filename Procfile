release: python manage.py migrate
worker: celery worker -A cfabib -l info
web: gunicorn cfabib.wsgi --log-file -