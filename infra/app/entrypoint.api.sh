#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py migrate

exec "$@"
