#!/bin/bash
if [[ ! -d './rematch/migrations' ]];
then
  echo "first time, migrating"
  python manage.my makemigrations collab
  python manage.py migrate
fi
./start_celery.sh &
uwsgi --socket :8001 --module rematch.wsgi &
./start_nginx.sh
