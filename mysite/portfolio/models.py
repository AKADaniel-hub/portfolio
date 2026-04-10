from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    descricao = models.TextField()
    duracao_anos = models.IntegerField()
    universidade = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    pagina_lusofona = models.URLField()

    def __str__(self):
        return self.nome


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    website = models.URLField()

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    tecnologias = models.ManyToManyField(Tecnologia)  # 🔥 RELAÇÃO
    github_link = models.URLField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_demo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome


class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE
    )

    orientadores = models.ManyToManyField(Docente)  # 🔥 RELAÇÃO
    tecnologias = models.ManyToManyField(Tecnologia)  # 🔥 RELAÇÃO

    pdf = models.URLField()
    imagem = models.URLField(blank=True)

    resumo = models.TextField()
    palavras_chave = models.TextField()
    areas = models.TextField()

    classificacao = models.IntegerField()

    def __str__(self):
        return self.titulo