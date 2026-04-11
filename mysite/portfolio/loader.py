import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portfolio.models import TFC, Tecnologia, Licenciatura

JSON_FILE = os.path.join(BASE_DIR, 'data', 'trabalhos_2025.json')


def get_or_create_tecnologia(nome):
    nome = nome.strip().rstrip(".")
    if not nome:
        return None
    tec, created = Tecnologia.objects.get_or_create(
        nome=nome,
        defaults={
            'tipo': 'outro',
            'descricao': '',
            'url_website': '',
            'nivel_interesse': 3,   # ← obrigatório no teu modelo
            'ano_inicio': 2024,     # ← obrigatório no teu modelo
            'em_uso': True,
        }
    )
    if created:
        print(f"  [+] Tecnologia criada: {nome}")
    return tec


def get_or_create_licenciatura(nome):
    nome = nome.strip() if nome else ""
    if not nome:
        return None
    lic, created = Licenciatura.objects.get_or_create(
        nome=nome,
        defaults={
            "sigla": "", "grau": "", "area_cientifica": "",
            "duracao_anos": 0, "ects_total": 0, "descricao": "",
            "url_lusofona": "", "ano_inicio": 0, "universidade": ""
        }
    )
    if created:
        print(f"  [+] Licenciatura criada: {nome}")
    return lic

def load_tfcs():
    with open(JSON_FILE, encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    criados = 0
    atualizados = 0

    for i, entry in enumerate(data, start=1):
        titulo = entry.get('titulo', '').strip()
        if not titulo:
            print(f"[{i}/{total}] Ignorado (sem título)")
            continue

        rating = 0
        try:
            rating = int(entry.get('rating', 0))
        except (ValueError, TypeError):
            pass

        lic = get_or_create_licenciatura(entry.get('licenciatura'))

        defaults = {
            'descricao':      entry.get('resumo', '') or '',
            'ano':            0,
            'autor':          entry.get('autor', '') or '',
            'orientador':     entry.get('orientador', '') or '',
            'licenciatura':   lic,                              # ← adiciona
            'pdf':            entry.get('pdf', '') or '',
            'imagem':         entry.get('imagem', '') or '',
            'resumo':         entry.get('resumo', '') or '',
            'palavras_chave': entry.get('palavras_chave', '') or '',
            'areas':          entry.get('areas', '') or '',
            'classificacao':  rating,
            'url_repositorio': '',
            'destaque':       rating >= 4,
        }

        tfc, created = TFC.objects.get_or_create(titulo=titulo, defaults=defaults)

        if not created:
            for field, value in defaults.items():
                setattr(tfc, field, value)
            tfc.save()
            atualizados += 1
            status = 'atualizado'
        else:
            criados += 1
            status = 'criado'

        tfc.tecnologias.clear()
        tecnologias_raw = entry.get('tecnologias', '') or ''
        for nome_tec in tecnologias_raw.split(';'):
            nome_tec = nome_tec.strip().rstrip(".")
            if nome_tec:
                tec = get_or_create_tecnologia(nome_tec)
                if tec:
                    tfc.tecnologias.add(tec)

        print(f"[{i}/{total}] {status.upper()}: {titulo}")

    print(f"\nConcluído: {criados} criados, {atualizados} atualizados, {total} total.")


if __name__ == '__main__':
    load_tfcs()