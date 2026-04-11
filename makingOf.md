# Making Of — Portfolio Django

## Diário de Bordo — Modelação da Base de Dados

---

## 1. Primeiro Esboço

O modelo inicial foi desenhado à mão antes de começar a programar, para identificar as principais entidades do sistema:

![alt text](<images/Sem título.jpg>)

**Decisões iniciais:**
- O campo `tecnologias` começou como texto simples, mas foi alterado para **ManyToMany** para permitir filtros e reutilização
- `Docente` foi separado do utilizador para permitir guardar docentes mesmo sem conta na plataforma

---

## 2. Evolução do Modelo

### Versão 1 — Modelo Inicial

```python
class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano = models.IntegerField()
    descricao = models.TextField()
    classificacao = models.IntegerField()
```

**Problemas:**
- Não estava ligado a `Licenciatura` → não dava para filtrar por curso  
- Faltavam vários campos importantes (orientador, pdf, resumo, etc.)  
- Não tinha imagem (capa do TFC)

---

### Versão 2 — Com Orientadores

```python
class TFC(models.Model):
    ...
    orientadores = models.ManyToManyField(Docente)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE)
```

**Problemas:**
- Os orientadores vinham como **texto no JSON**, não como objetos  
- O sistema associava **todos os docentes a todos os TFCs**  
- Uso de `get_or_create` causava associações erradas  

**Correção:**
- `orientador` passou a **CharField (texto simples)**  
- `Docente` mantém-se como entidade separada (para UCs)

---

### Versão 3 — Modelo Final

```python
class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    orientador = models.CharField(max_length=500, blank=True)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.SET_NULL, null=True)
    pdf = models.URLField(blank=True)
    imagem = models.URLField(blank=True)
    resumo = models.TextField(blank=True)
    palavras_chave = models.TextField(blank=True)
    areas = models.TextField(blank=True)
    classificacao = models.IntegerField(default=0)
    destaque = models.BooleanField(default=False)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True)
```

---

## 3. Erros e Correções

### Erro 1 — `django.setup()` no sítio errado

**Problema:** código do `loader.py` foi colocado dentro do `models.py`  

**Erro:**
```
RuntimeError: populate() isn't reentrant
```

**Solução:** corrigir o `models.py`

---

### Erro 2 — Tecnologias com ponto final

**Problema:** `"Python."` e `"Python"` eram tratadas como diferentes  

**Solução:**
```python
def clean_list(text):
    text = text.strip().rstrip(".")
    return [x.strip().rstrip(".") for x in text.replace(",", ";").split(";") if x.strip()]
```

---

### Erro 3 — Licenciaturas duplicadas

**Problema:** nomes diferentes para o mesmo curso → duplicação  

**Solução:** criar um mapeamento para unificar

```python
LICENCIATURAS = {
    'lei': ('Licenciatura em Engenharia Informática', 'LEI', 'licenciatura'),
}
```

---

### Erro 4 — Semestre como texto

**Problema:** `"1º Semestre"` em vez de número  

**Solução:**
```python
def parse_semestre(valor):
    if isinstance(valor, int):
        return valor
    if '1' in str(valor):
        return 1
    if '2' in str(valor):
        return 2
    return 1
```

---

### Erro 5 — Emails dos docentes

**Problema:** emails não aparecem diretamente (JavaScript)  

**Solução:**
```python
span = soup.select_one('span.copy-button[address][domain]')
email = f"{span['address']}@{span['domain']}"
```

---

## 4. Decisões de Modelação

### Licenciatura
- **ForeignKey** → cada TFC/UC pertence a um curso  
- Campo `grau` → permite filtrar facilmente  

### Docente
- Separado de `orientador`  
- **ManyToMany com UC**  

### Tecnologia
- Reutilizável (evita duplicados)  
- Campo `tipo`  

### TFC
- `orientador` como texto  
- `destaque` automático  

### Projeto
- Ligado a UC  
- Data opcional  

### Competência
- **ManyToMany com Tecnologia e Projeto**  

---

## 5. Estrutura Final do Modelo

![alt text](<images/Sem título1.jpg>)

---

## 6. Scripts Criados

| Script | Função |
|---|---|
| `loader.py` | Importa TFCs |
| `load_ucs_projetos_docentes.py` | Importa UCs, Projetos e Docentes |
| `fix_licenciaturas.py` | Corrige duplicações |
| `load_competencias.py` | Adiciona competências |
| `scraper_docentes.py` | Extrai docentes |
| `scraper_ucs.py` | Extrai UCs |
| `scraper_projetos.py` | Extrai projetos |
| `setup.sh` | Limpa BD e executa tudo |
