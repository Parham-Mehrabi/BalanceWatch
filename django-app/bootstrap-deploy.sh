python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn balance_watch.wsgi --bind 0.0.0.0:8000 --access-logfile - --error-logfile - --workers 3 --threads 2


