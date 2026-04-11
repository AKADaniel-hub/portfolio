import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portfolio.models import Licenciatura, TFC, UnidadeCurricular

# Mapeamento sigla → nome completo correto
LICENCIATURAS = {
    'lei':      ('Licenciatura em Engenharia Informática',      'LEI',      'licenciatura'),
    'meisi':    ('Mestrado em Engenharia Informática e Sistemas de Informação', 'MEISI', 'mestrado'),
    'mcid':     ('Mestrado em Comunicação, Cultura e Tecnologias de Informação', 'MCID', 'mestrado'),
    'mcid-sig': ('Mestrado em Comunicação, Cultura e Tecnologias de Informação - SIG', 'MCID-SIG', 'mestrado'),
    'di':       ('Doutoramento em Informática',                 'DI',       'doutoramento'),
    'lig':      ('Licenciatura em Informática de Gestão',       'LIG',      'licenciatura'),
    'leirt':    ('Licenciatura em Engenharia Informática e Redes de Telecomunicações', 'LEIRT', 'licenciatura'),
    'licma':    ('Licenciatura em Ciência de Dados',            'LICMA',    'licenciatura'),
    'lcid':     ('Licenciatura em Ciência e Informática de Dados', 'LCID',  'licenciatura'),
}

def merge_licenciaturas():
    for sigla_lower, (nome_completo, sigla, grau) in LICENCIATURAS.items():

        # Garante que existe UMA licenciatura correta
        lic_principal, _ = Licenciatura.objects.update_or_create(
            sigla=sigla,
            defaults={
                'nome':          nome_completo,
                'grau':          grau,
                'universidade':  'Universidade Lusófona',
                'area_cientifica': 'Informática',
                'duracao_anos':  3 if grau == 'licenciatura' else 2 if grau == 'mestrado' else 4,
                'ects_total':    180 if grau == 'licenciatura' else 120 if grau == 'mestrado' else 240,
            }
        )
        print(f"[OK] {sigla} → {nome_completo}")

        # Redireciona TFCs que usam variantes do nome
        nomes_variantes = Licenciatura.objects.filter(
            nome__icontains=sigla_lower
        ).exclude(pk=lic_principal.pk)

        for lic_old in nomes_variantes:
            tfcs = TFC.objects.filter(licenciatura=lic_old)
            ucs  = UnidadeCurricular.objects.filter(licenciatura=lic_old)
            print(f"  Migrar {tfcs.count()} TFCs e {ucs.count()} UCs de '{lic_old}' → '{lic_principal}'")
            tfcs.update(licenciatura=lic_principal)
            ucs.update(licenciatura=lic_principal)
            lic_old.delete()

        # Redireciona também pelo nome completo
        dups = Licenciatura.objects.filter(
            nome=nome_completo
        ).exclude(pk=lic_principal.pk)

        for lic_old in dups:
            TFC.objects.filter(licenciatura=lic_old).update(licenciatura=lic_principal)
            UnidadeCurricular.objects.filter(licenciatura=lic_old).update(licenciatura=lic_principal)
            print(f"  Removido duplicado: '{lic_old.nome}'")
            lic_old.delete()

    print(f"\nTotal de licenciaturas: {Licenciatura.objects.count()}")


if __name__ == '__main__':
    merge_licenciaturas()