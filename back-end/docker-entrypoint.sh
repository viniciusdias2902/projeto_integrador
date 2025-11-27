#!/bin/bash

echo "Aguardando PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done

echo "PostgreSQL pronto!"

echo "Rodando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Criando superusuário se não existir..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin@admin.com', 'admin@admin.com', 'admin123')
    print('Superusuário criado!')
else:
    print('Superusuário já existe.')
EOF

echo "Iniciando servidor..."
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 4