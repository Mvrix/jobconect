
from app_dash import views
from django.urls import path

urlpatterns = [
path('', views.home, name='home'),
path('login_candidato/', views.login_candidato, name='login_candidato'),
path('login_empresa/', views.login_empresa, name='login_empresa'),
path('cadastro_candidato/', views.cadastro_candidato_view,
        name='cadastro_candidato'),
path('cadastro_empresa/', views.cadastro_empresa_view, name='cadastro_empresa'),
path('home_empresa/', views.pagina_apos_cadastro_empresa,
        name='pagina_apos_cadastro_empresa'),
path('home_candidato/', views.pagina_apos_cadastro_candidato,
        name='pagina_apos_cadastro_candidato'),
path('logout/', views.custom_logout, name='logout'),
path('vagas/', views.lista_vagas, name='lista_vagas'),
path('vagas/<int:vaga_id>/candidatos/',
        views.visualizar_candidatos, name='visualizar_candidatos'),
path('vagas/nova/', views.nova_vaga, name='nova_vaga'),
path('vagas/<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
path('vagas/<int:vaga_id>/deletar/',
        views.deletar_vaga, name='deletar_vaga'),
path('vagas/<int:vaga_id>/candidatar/',
        views.candidatar_vaga, name='candidatar_vaga'),
path('desistir_vaga/<int:candidatura_id>/',
        views.desistir_vaga, name='desistir_vaga'),
path('vagas_criadas_por_mes/', views.vagas_criadas_por_mes, name='vagas_criadas_por_mes'),
path('candidatos_recebidos_por_mes/', views.candidatos_recebidos_por_mes, name='candidatos_recebidos_por_mes'),
]
