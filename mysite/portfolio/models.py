from django.db import models

from django.db import models



class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    descricao = models.TextField()
    duracao_anos = models.IntegerField()
    universidade = models.CharField(max_length=200)

    def __str__(self):
        return self.nome



class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    semestre = models.IntegerField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='uc_imagens/', blank=True, null=True)

    def __str__(self):
        return self.nome



class Docente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    pagina_lusofona = models.URLField()

    def __str__(self):
        return self.nome



class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    tecnologias = models.TextField()  # simples (podes melhorar depois com relação)
    github_link = models.URLField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_demo = models.URLField(blank=True, null=True)

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



class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField()  # podes usar 1-5 por exemplo
    descricao = models.TextField()

    def __str__(self):
        return self.nome



class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField()

    def __str__(self):
        return self.nome



class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano = models.IntegerField()
    descricao = models.TextField()
    classificacao = models.IntegerField()

    def __str__(self):
        return self.titulo