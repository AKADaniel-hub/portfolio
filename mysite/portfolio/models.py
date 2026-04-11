from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Licenciatura(models.Model):
    GRAU_CHOICES = [
        ('licenciatura', 'Licenciatura'),
        ('mestrado', 'Mestrado'),
        ('doutoramento', 'Doutoramento'),
        ('ctesp', 'CTeSP'),
    ]
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    grau = models.CharField(max_length=20, choices=GRAU_CHOICES, blank=True)
    area_cientifica = models.CharField(max_length=200, blank=True)
    duracao_anos = models.IntegerField(default=0)
    ects_total = models.IntegerField(default=0)
    descricao = models.TextField(blank=True)
    url_lusofona = models.URLField(blank=True)
    logo = models.ImageField(upload_to='licenciatura/', blank=True, null=True)
    ano_inicio = models.IntegerField(default=0)
    universidade = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.sigla} - {self.nome}" if self.sigla else self.nome

    class Meta:
        verbose_name = 'Licenciatura'
        verbose_name_plural = 'Licenciaturas'


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    url_lusofona = models.URLField(blank=True)
    foto = models.ImageField(upload_to='docentes/', blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'


class Tecnologia(models.Model):
    TIPO_CHOICES = [
        ('linguagem', 'Linguagem de Programação'),
        ('framework', 'Framework'),
        ('biblioteca', 'Biblioteca'),
        ('ferramenta', 'Ferramenta'),
        ('base_dados', 'Base de Dados'),
        ('outro', 'Outro'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outro')
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    url_website = models.URLField(blank=True)
    nivel_interesse = models.IntegerField(default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    ano_inicio = models.IntegerField(default=0)
    em_uso = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'


class UnidadeCurricular(models.Model):
    SEMESTRE_CHOICES = [(1, '1º Semestre'), (2, '2º Semestre')]
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    ano_curricular = models.IntegerField()
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES)
    ects = models.IntegerField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)
    codigo = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    licenciatura = models.ForeignKey(
        Licenciatura, on_delete=models.CASCADE, related_name='unidades_curriculares')
    docentes = models.ManyToManyField(Docente, blank=True, related_name='unidades_curriculares')

    def __str__(self):
        return f"{self.sigla} - {self.nome}"

    class Meta:
        verbose_name = 'Unidade Curricular'
        verbose_name_plural = 'Unidades Curriculares'


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_demo = models.URLField(blank=True)
    repositorio_github = models.URLField(blank=True)
    data_realizacao = models.DateField(null=True, blank=True)
    classificacao = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    destaque = models.BooleanField(default=False)
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular, on_delete=models.CASCADE,
        related_name='projetos', null=True, blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='projetos')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.TextField(blank=True)
    ano = models.IntegerField(default=0)
    autor = models.CharField(max_length=200)
    orientador = models.CharField(max_length=500, blank=True)
    licenciatura = models.ForeignKey(        # ← adiciona isto
        Licenciatura, on_delete=models.SET_NULL, null=True, blank=True)
    url_repositorio = models.URLField(blank=True)
    pdf = models.URLField(blank=True)
    imagem = models.URLField(blank=True)
    resumo = models.TextField(blank=True)
    palavras_chave = models.TextField(blank=True)
    areas = models.TextField(blank=True)
    classificacao = models.IntegerField(default=0)
    destaque = models.BooleanField(default=False)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='tfcs')

    def __str__(self):
        return self.titulo
        
    class Meta:
        verbose_name = 'TFC'
        verbose_name_plural = 'TFCs'


class Competencia(models.Model):
    TIPO_CHOICES = [
        ('tecnica', 'Técnica'),
        ('transversal', 'Transversal'),
        ('soft', 'Soft Skill'),
    ]
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    nivel = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='competencias')
    projetos = models.ManyToManyField(Projeto, blank=True, related_name='competencias')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Competência'
        verbose_name_plural = 'Competências'


class Formacao(models.Model):
    TIPO_CHOICES = [
        ('curso', 'Curso'), ('workshop', 'Workshop'),
        ('certificacao', 'Certificação'), ('mooc', 'MOOC'), ('outro', 'Outro'),
    ]
    titulo = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    certificado = models.ImageField(upload_to='formacoes/', blank=True, null=True)
    url = models.URLField(blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='formacoes')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Formação'
        verbose_name_plural = 'Formações'

