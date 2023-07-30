
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Candidato, Empresa, User, UserProfile, Vaga


def home(request):
    return render(request, 'home.html')

def vagas_criadas_por_mes(request):
    vagas_por_mes = Vaga.objects.annotate(mes_criacao=TruncMonth('data_criacao')) \
                                .values('mes_criacao') \
                                .annotate(count=Count('id'))

    data = [{'mes': item['mes_criacao'].strftime('%Y-%m'), 'count': item['count']} for item in vagas_por_mes]

    return JsonResponse(data, safe=False)

def candidatos_recebidos_por_mes(request):
    candidatos_por_mes = Candidato.objects.annotate(mes_candidatura=TruncMonth('data_candidatura')) \
                                        .values('mes_candidatura') \
                                        .annotate(count=Count('id'))

    data = [{'mes': item['mes_candidatura'].strftime('%Y-%m'), 'count': item['count']} for item in candidatos_por_mes]

    return JsonResponse(data, safe=False)


def lista_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, "empresa/vagas/lista_vagas.html", {"vagas": vagas})


def visualizar_candidatos(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    candidatos = Candidato.objects.filter(vaga=vaga)

    for candidato in candidatos:
        candidato.pontuacao_total = candidato.pontuacao_faixa_salarial + \
            candidato.pontuacao_escolaridade

    return render(
        request, "empresa/vagas/visualizar_candidatos.html", {
            "vaga": vaga,
            "candidatos": candidatos,
        }
    )


def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)

    if request.method == 'POST':
        vaga.delete()
        return redirect('lista_vagas')

    return render(request, 'empresa/vagas/deletar_vaga.html', {'vaga': vaga})


def login_empresa(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                error = "Usuário ou senha incorretos."
                return render(request, "empresa/login_empresa.html", {"error": error})

            if user_profile.user_type == 'E':
                login(request, user)
                return redirect("pagina_apos_cadastro_empresa")
            else:
                error = "Apenas empresas podem fazer login."
                return render(request, "empresa/login_empresa.html", {"error": error})
        else:
            error = "Usuário ou senha incorretos."
            return render(request, "empresa/login_empresa.html", {"error": error})

    return render(request, "empresa/login_empresa.html")


def login_candidato(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                error = "Usuário ou senha incorretos."
                return render(request, "candidato/login_candidato.html", {"error": error})

            if user_profile.user_type == 'C':
                login(request, user)
                return redirect("pagina_apos_cadastro_candidato")
            else:
                error = "Apenas candidatos podem fazer login."
                return render(request, "candidato/login_candidato.html", {"error": error})
        else:
            error = "Usuário ou senha incorretos."
            return render(request, "candidato/login_candidato.html", {"error": error})

    return render(request, "candidato/login_candidato.html")


def cadastro_candidato_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = 'C'
        
        if User.objects.filter(username=username).exists():
            error = "Este nome de usuário já está sendo usado por outro usuário."
            return render(request, "cadastro/cadastro_candidato.html", {"error": error})

        if password1 != password2:
            return render(
                request,
                "cadastro/cadastro_candidato.html",
                {"error": "As senhas não coincidem."},
            )


        user = User.objects.create_user(
            username=username, password=password1)
        UserProfile.objects.create(user=user, user_type=user_type)

        return redirect("login_candidato")

    return render(request, "cadastro/cadastro_candidato.html")


def cadastro_empresa_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        nome_empresa = request.POST.get("nome_empresa")
        cnpj = request.POST.get("cnpj")

        if password1 != password2:
            return render(
                request,
                "cadastro/cadastro_empresa.html",
                {"error": "As senhas não coincidem."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "cadastro/cadastro_empresa.html",
                {"error": "Este e-mail já está sendo usado por outra empresa."},
            )

        user = User.objects.create_user(username=username, password=password1)
        empresa = Empresa.objects.create(nome_empresa=nome_empresa, cnpj=cnpj)

        user_profile = UserProfile.objects.create(user=user, user_type='E')

        return redirect("login_empresa")

    return render(request, "cadastro/cadastro_empresa.html")


def custom_logout(request):
    logout(request)
    return redirect('home')


@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        faixa_salarial = request.POST.get('faixa_salarial')
        requisitos = request.POST.get('requisitos')
        escolaridade_minima = request.POST.get('escolaridade_minima')

        vaga.nome = nome
        vaga.faixa_salarial = faixa_salarial
        vaga.requisitos = requisitos
        vaga.escolaridade_minima = escolaridade_minima

        vaga.save()

        candidatos = Candidato.objects.filter(vaga=vaga)
        pontuacao_escolaridade_dict = {
            'EF': 0,
            'EM': 1,
            'TEC': 2,
            'ES': 3,
            'POS': 4,
            'DOUT': 5,
        }

        for candidato in candidatos:
            candidato.pontuacao_faixa_salarial = 0
            if candidato.pretensao_salarial == vaga.faixa_salarial:
                candidato.pontuacao_faixa_salarial = 1

            pontuacao_escolaridade = 0
            if pontuacao_escolaridade_dict[candidato.escolaridade] >= pontuacao_escolaridade_dict[vaga.escolaridade_minima]:
                pontuacao_escolaridade = 1

            candidato.pontuacao_escolaridade = pontuacao_escolaridade
            candidato.pontuacao_total = candidato.pontuacao_faixa_salarial + pontuacao_escolaridade
            candidato.save()

        return redirect('lista_vagas')

    return render(request, 'empresa/vagas/editar_vaga.html', {'vaga': vaga})


@login_required
def pagina_apos_cadastro_empresa(request):
    vagas = Vaga.objects.all()

    empresa = Empresa.objects.first()
    
    return render(request, "empresa/home_empresa.html", {"vagas": vagas, "empresa": empresa})


@login_required
def pagina_apos_cadastro_candidato(request):
    vagas = Vaga.objects.all()

    vagas_candidatadas = Candidato.objects.filter(user=request.user)

    ids_vagas_candidatadas = vagas_candidatadas.values_list(
        'vaga__id', flat=True)

    vagas_disponiveis = vagas.exclude(id__in=ids_vagas_candidatadas)

    return render(request, "candidato/home_candidato.html", {"vagas": vagas_disponiveis, "vagas_candidatadas": vagas_candidatadas})


@login_required
def nova_vaga(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        faixa_salarial = request.POST.get('faixa_salarial')
        requisitos = request.POST.get('requisitos')
        escolaridade_minima = request.POST.get('escolaridade_minima')

        nova_vaga = Vaga.objects.create(
            nome=nome,
            faixa_salarial=faixa_salarial,
            requisitos=requisitos,
            escolaridade_minima=escolaridade_minima,
        )

        nova_vaga.save()

        return redirect('pagina_apos_cadastro_empresa')


    return render(request, 'empresa/vagas/nova_vaga.html')


@login_required
def desistir_vaga(request, candidatura_id):
    candidatura = get_object_or_404(
        Candidato, pk=candidatura_id, user=request.user)

    if request.method == 'POST':
        candidatura.delete()
        messages.success(request, 'Você desistiu da vaga com sucesso!')
        return redirect('pagina_apos_cadastro_candidato')

    return redirect('pagina_apos_cadastro_candidato')


@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)

    if Candidato.objects.filter(user=request.user, vaga=vaga).exists():
        return redirect('pagina_apos_cadastro_candidato')

    if request.method == 'POST':
        pretensao_salarial = request.POST.get('pretensao_salarial')
        experiencia = request.POST.get('experiencia')
        escolaridade = request.POST.get('escolaridade')

        pontuacao_faixa_salarial = 0
        if pretensao_salarial == vaga.faixa_salarial:
            pontuacao_faixa_salarial = 1

        pontuacao_escolaridade_dict = {
            'EF': 0,
            'EM': 1,
            'TEC': 2,
            'ES': 3,
            'POS': 4,
            'DOUT': 5,
        }

        pontuacao_escolaridade = 0
        if pontuacao_escolaridade_dict[escolaridade] >= pontuacao_escolaridade_dict[vaga.escolaridade_minima]:
            pontuacao_escolaridade = 1

        pontuacao_total = pontuacao_faixa_salarial + pontuacao_escolaridade

        candidato = Candidato.objects.create(
            pretensao_salarial=pretensao_salarial,
            experiencia=experiencia,
            escolaridade=escolaridade,
            vaga=vaga,
            user=request.user,
            pontuacao_faixa_salarial=pontuacao_faixa_salarial,
            pontuacao_escolaridade=pontuacao_escolaridade,
            pontuacao_total=pontuacao_total,
        )

        messages.success(request, 'Candidatura realizada com sucesso!')
        return HttpResponseRedirect(reverse('pagina_apos_cadastro_candidato'))

    return render(request, 'candidato/vagas/candidatar_vaga.html', {'vaga': vaga})
