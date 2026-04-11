#!/bin/bash
set -e

echo "=== A apagar DB e migrações ==="
rm -f db.sqlite3
find . -path "*/migrations/0*.py" -delete

echo "=== A criar migrações e migrar ==="
python manage.py makemigrations
python manage.py migrate

echo "=== A criar superuser ==="
python manage.py createsuperuser

echo "=== A carregar TFCs ==="
python portfolio/loader.py

echo "=== A carregar Docentes, UCs e Projetos ==="
python portfolio/load_ucs_projetos_docentes.py

echo "=== A corrigir Licenciaturas ==="
python portfolio/fix_licenciaturas.py


echo "=== A carregar Competências ==="
python portfolio/load_competencias.py

echo "=== Tudo pronto! ==="
