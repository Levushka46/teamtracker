#!/bin/bash

set -e
# python3 -m http.server --bind 0.0.0.0

# Wait for PostgreSQL service to accept connections
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  # Wait for 5 seconds before checking again
  sleep 5
done
echo "Database is now available"

python3 manage.py compilemessages
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
exec "$@"