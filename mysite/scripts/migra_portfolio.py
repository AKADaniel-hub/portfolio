"""
Migração de ficheiros locais em media/ para Cloudinary.
App: portfolio
"""
import os
from django.core.files import File

from portfolio.models import (
    Licenciatura,
    Docente,
    Tecnologia,
    UnidadeCurricular,
    Projeto,
    Formacao,
)


def migra(queryset, campo: str):
    """Itera o queryset e faz re-save do campo `campo` (ImageField)."""
    modelo = queryset.model.__name__
    total = 0
    falhas = 0

    for obj in queryset:
        img = getattr(obj, campo, None)
        if not img or not img.name:
            continue

        try:
            local_path = img.path  # caminho no disco (media/)
        except (NotImplementedError, ValueError):
            # Já está num storage remoto, ou sem ficheiro local
            print(f"[skip] {modelo}({obj.pk}) -> sem path local")
            continue

        if not os.path.exists(local_path):
            print(f"[skip] {modelo}({obj.pk}) -> ficheiro não existe: {local_path}")
            falhas += 1
            continue

        with open(local_path, "rb") as f:
            getattr(obj, campo).save(
                os.path.basename(local_path),
                File(f),
                save=True,
            )
        total += 1
        print(f"[ok]   {modelo}({obj.pk}) -> {campo} migrado")

    print(f"\n== {modelo}.{campo}: migrados {total} | falhas {falhas} ==\n")


def run():
    print("\n>>> A migrar ficheiros do portfolio para Cloudinary <<<\n")
    migra(Licenciatura.objects.all(),      "logo")
    migra(Docente.objects.all(),           "foto")
    migra(Tecnologia.objects.all(),        "logo")
    migra(UnidadeCurricular.objects.all(), "imagem")
    migra(Projeto.objects.all(),           "imagem")
    migra(Formacao.objects.all(),          "certificado")
    print(">>> Concluído <<<\n")


# Permite executar com `import scripts.migra_portfolio`
run()