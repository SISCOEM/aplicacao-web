#!/bin/bash

sleep 4

# Comandos adicionais do Django
python manage.py migrate --fake contenttypes
python manage.py migrate
python manage.py collectstatic --noinput

python3 /code/execute_sql.py
# Executa o comando padrão
exec "$@"

