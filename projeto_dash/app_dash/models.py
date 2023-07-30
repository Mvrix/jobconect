

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('C', 'Candidato'),
        ('E', 'Empresa'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=1, choices=USER_TYPE_CHOICES, default='C')

    def __str__(self):
        return self.user.username


class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)

    def __str__(self):
        return self.nome_empresa


class Vaga(models.Model):
    FAIXA_SALARIAL_CHOICES = [
        ('1', 'Até 1.000'),
        ('2', 'De 1.000 a 2.000'),
        ('3', 'De 2.000 a 3.000'),
        ('4', 'Acima de 3.000'),
    ]
    ESCOLARIDADE_CHOICES = [
        ('EF', 'Ensino Fundamental'),
        ('EM', 'Ensino Médio'),
        ('TEC', 'Tecnólogo'),
        ('ES', 'Ensino Superior'),
        ('POS', 'Pós / MBA / Mestrado'),
        ('DOUT', 'Doutorado'),
    ]

    nome = models.CharField(max_length=255)
    faixa_salarial = models.CharField(
        max_length=1, choices=FAIXA_SALARIAL_CHOICES)
    requisitos = models.TextField()
    escolaridade_minima = models.CharField(
        max_length=4, choices=ESCOLARIDADE_CHOICES)

    def __str__(self):
        return self.nome

    def vagas_disponiveis(self, user):

        candidaturas = Candidato.objects.filter(
            user=user).values_list('vaga', flat=True)
        return Vaga.objects.exclude(pk__in=candidaturas)
    
    data_criacao = models.DateTimeField(default=timezone.now)


class Candidato(models.Model):
    PRETENSAO_SALARIAL_CHOICES = [
        ('1', 'Até 1.000'),
        ('2', 'De 1.000 a 2.000'),
        ('3', 'De 2.000 a 3.000'),
        ('4', 'Acima de 3.000'),
    ]

    EXPERIENCIA_CHOICES = [
        ('1', 'Sem Experiência'),
        ('2', 'Menos de 1 ano'),
        ('3', '1 a 3 anos'),
        ('4', '3 a 5 anos'),
        ('5', 'Mais de 5 anos'),
    ]

    ESCOLARIDADE_CHOICES = [
        ('EF', 'Ensino Fundamental'),
        ('EM', 'Ensino Médio'),
        ('TEC', 'Tecnólogo'),
        ('ES', 'Ensino Superior'),
        ('POS', 'Pós / MBA / Mestrado'),
        ('DOUT', 'Doutorado'),
    ]

    pretensao_salarial = models.CharField(
        max_length=1, choices=PRETENSAO_SALARIAL_CHOICES)
    experiencia = models.CharField(max_length=1, choices=EXPERIENCIA_CHOICES)
    escolaridade = models.CharField(max_length=4, choices=ESCOLARIDADE_CHOICES)
    perfil = models.TextField()
    vaga = models.ForeignKey(
        Vaga, on_delete=models.CASCADE, related_name='candidatos')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='candidaturas')
    pontuacao_faixa_salarial = models.IntegerField(default=0)
    pontuacao_escolaridade = models.IntegerField(default=0)
    pontuacao_total = models.IntegerField(default=0)
    data_candidatura = models.DateTimeField(default=timezone.now)
    

    def calcular_pontuacao_total(self):
        return self.pontuacao_faixa_salarial + self.pontuacao_escolaridade

    def __str__(self):
        return f"Candidato {self.user.email} para a vaga {self.vaga.nome}"
