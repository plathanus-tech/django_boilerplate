#!/bin/sh
set -e

# This script is ran only by the db_migration container. This speeds up the startup of the application

echo "Collecting static files.."
python manage.py collectstatic --noinput

echo "Compiling messages..."
python manage.py compilemessages

exec "$@"
