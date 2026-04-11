import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portfolio.models import Competencia

COMPETENCIAS = [
    {'nome': 'Programação',      'tipo': 'tecnica',     'nivel': 5, 'descricao': ''},
    {'nome': 'Cibersegurança',   'tipo': 'tecnica',     'nivel': 3, 'descricao': ''},
    {'nome': 'Criatividade',     'tipo': 'soft',        'nivel': 4, 'descricao': ''},
    {'nome': 'Adaptabilidade',   'tipo': 'soft',        'nivel': 5, 'descricao': ''},
    {'nome': 'Trabalho em Equipa', 'tipo': 'soft',      'nivel': 5, 'descricao': ''},
    {'nome': 'Liderança',        'tipo': 'soft',        'nivel': 5, 'descricao': ''},
]

for c in COMPETENCIAS:
    obj, created = Competencia.objects.get_or_create(
        nome=c['nome'],
        defaults={'tipo': c['tipo'], 'nivel': c['nivel'], 'descricao': c['descricao']}
    )
    print(f"{'[+]' if created else '[=]'} {obj.nome}")

print(f"\nTotal: {Competencia.objects.count()} competências.")