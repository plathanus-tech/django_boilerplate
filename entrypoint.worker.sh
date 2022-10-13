#!/bin/sh
set -e

if [ "$DJANGO_SETTINGS_MODULE" = "app.settings.dev" ]
then

    while ! nc -z $SQL_HOST $SQL_PORT; do
        echo "Waiting for postgres... $SQL_HOST $SQL_PORT"
        sleep 5
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py compilemessages -v 0

exec "$@"
