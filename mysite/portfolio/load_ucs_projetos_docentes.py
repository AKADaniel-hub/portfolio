import os
import sys
import json
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portfolio.models import Docente, Tecnologia, UnidadeCurricular, Projeto, Licenciatura

DATA_DIR = os.path.join(BASE_DIR, 'data')


def parse_semestre(valor):
    if isinstance(valor, int):
        return valor
    if '1' in str(valor):
        return 1
    if '2' in str(valor):
        return 2
    return 1


def load_docentes():
    path = os.path.join(DATA_DIR, 'docentes.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    criados = 0
    for item in data:
        doc, created = Docente.objects.get_or_create(
            nome=item['nome'],
            defaults={
                'email':        item.get('email', ''),
                'url_lusofona': item.get('url_lusofona', ''),
            }
        )
        if created:
            criados += 1
            print(f"  [+] Docente: {doc.nome}")

    print(f"\nDocentes: {criados} criados de {len(data)} total.")


def load_ucs():
    path = os.path.join(DATA_DIR, 'unidades_curriculares.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    criados = 0
    for item in data:
        lic, _ = Licenciatura.objects.get_or_create(
            nome=item.get('curso_nome', item.get('curso', '')),
            defaults={
                'sigla':         item.get('curso', '').upper(),
                'grau':          '',
                'area_cientifica': '',
                'duracao_anos':  0,
                'ects_total':    0,
                'descricao':     '',
                'url_lusofona':  '',
                'ano_inicio':    0,
                'universidade':  'Universidade Lusófona',
            }
        )

        uc, created = UnidadeCurricular.objects.get_or_create(
            codigo=item.get('codigo', ''),
            defaults={
                'nome':           item.get('nome', ''),
                'sigla':          item.get('sigla', ''),
                'ano_curricular': item.get('ano_curricular', 1),
                'semestre':       parse_semestre(item.get('semestre', 1)),
                'ects':           item.get('ects', 0),
                'descricao':      item.get('descricao', ''),
                'ativo':          item.get('ativo', True),
                'licenciatura':   lic,
            }
        )
        if created:
            criados += 1
            print(f"  [+] UC: {uc.nome}")

    print(f"\nUCs: {criados} criadas de {len(data)} total.")


def load_projetos():
    path = os.path.join(DATA_DIR, 'projetos.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    criados = 0
    for item in data:
        uc_info = item.get('uc', '')
        uc = None
        if uc_info:
            nome_uc = uc_info.split('(')[0].strip()
            uc = UnidadeCurricular.objects.filter(nome__icontains=nome_uc).first()

        proj, created = Projeto.objects.get_or_create(
            titulo=item.get('titulo', ''),
            defaults={
                'descricao':           item.get('descricao', ''),
                'conceitos_aplicados': item.get('conceitos_aplicados', ''),
                'video_demo':          item.get('video_demo', ''),
                'repositorio_github':  '',
                'classificacao':       0,
                'destaque':            False,
                'unidade_curricular':  uc,
                'data_realizacao':     date.today(),
            }
        )

        if created:
            for nome_tec in item.get('tecnologias', []):
                nome_tec = nome_tec.strip()
                if nome_tec:
                    tec, _ = Tecnologia.objects.get_or_create(
                        nome=nome_tec,
                        defaults={
                            'tipo':            'outro',
                            'descricao':       '',
                            'url_website':     '',
                            'nivel_interesse': 3,
                            'ano_inicio':      0,
                            'em_uso':          True,
                        }
                    )
                    proj.tecnologias.add(tec)
            criados += 1
            print(f"  [+] Projeto: {proj.titulo}")

    print(f"\nProjetos: {criados} criados de {len(data)} total.")


if __name__ == '__main__':
    print("=== A carregar Docentes ===")
    load_docentes()

    print("\n=== A carregar Unidades Curriculares ===")
    load_ucs()

    print("\n=== A carregar Projetos ===")
    load_projetos()

    print("\n✓ Tudo carregado!")