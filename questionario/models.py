from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

# Gerenciador para o usuário por e-mail
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# 1. Usuário Customizado (Login por E-mail)
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# 2. Perfil do Primeiro Acesso (Dados do Projeto Lagoa Mirim)
class Profile(models.Model):
    AGE_CHOICES = [
        ('A18', 'Até 18'), ('19_30', '19 a 30'), ('31_40', '31 a 40'),
        ('41_50', '41 a 50'), ('51_60', '51 a 60'), ('60+', '60+')
    ]
    GENDER_CHOICES = [
        ('MC', 'Mulher cisgênero'), ('HC', 'Homem cisgênero'),
        ('MT', 'Mulher transgênero'), ('HT', 'Homem transgênero'),
        ('NB', 'Pessoa não binária'), ('PNR', 'Prefiro não responder'), ('OUT', 'Outro')
    ]
    RACE_CHOICES = [
        ('IND', 'Indígena'), ('AFR', 'Afrodescendente/Preto(a)'),
        ('BRA', 'Branca(o)'), ('PAR', 'Mestiça(o)/Parda(o)'),
        ('ASI', 'Asiática(o)/Amarela(o)'), ('PNR', 'Prefiro não responder'), ('OUT', 'Outro')
    ]
    ORG_TYPE_CHOICES = [
        ('SOC', 'Sociedade civil organizada'), ('IND', 'Indivíduo'),
        ('GOV', 'Instituição governamental'), ('EDU', 'Centro educacional ou de pesquisa'),
        ('PRI', 'Setor produtivo ou privado'), ('OUT', 'Outros')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    nome_completo = models.CharField(max_length=255)
    email_contato = models.EmailField()
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    faixa_etaria = models.CharField(max_length=10, choices=AGE_CHOICES)
    genero = models.CharField(max_length=3, choices=GENDER_CHOICES)
    raca = models.CharField(max_length=3, choices=RACE_CHOICES)
    nome_organizacao = models.CharField(max_length=255)
    localidade_organizacao = models.CharField(max_length=255)
    tipo_organizacao = models.CharField(max_length=3, choices=ORG_TYPE_CHOICES)
    participou_projeto = models.BooleanField(default=False)

# 3. Estrutura das 7 Abas e Perguntas
class Aba(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    aba = models.ForeignKey(Aba, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.TextField()

    def __str__(self):
        return f"{self.aba.nome} - {self.texto[:30]}"

class Resposta(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    peso = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'pergunta')