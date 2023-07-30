# JobConect


Sistema em Django de vagas de emprego para o processo seletivo da JobConvo
Tela de vagas com número de candidatos, ser possível acessar quais candidatos (todos os dados) estão na vaga, Considere que a empresa tem o poder de editar ou deletar as vagas.

Bônus 1 (não obrigatório): conseguir pontuar quais candidatos estão dentro do perfil da vaga (faixa salarial + escolaridade). Ex:
Candidatos = 0 pontos
Se dentro da faixa salarial, adiciona 1 ponto
Se dentro ou acima da escolaridade, adiciona 1 ponto
Bônus 2 (não obrigatório): Tela para relatório: implantar o Charts js(ou semelhante) gerando os seguintes gráficos:
Vagas criadas por mês
Candidatos recebidos por mês

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

De que coisas você precisa para instalar o software e como instalá-lo?

```
VsCode ou outra IDE que suporte arquivos Python
```

### 🔧 Instalação

Autalmente o sistema já está com um banco de dados com informações, mas caso queria criar um banco sem nenhum dado, aqui está como fazer:

```
cd projeto_dash

python ./manage.py  makemigrations

python ./manage.py migrate
```

Caso altere o arquivo Models.py precisará realizar a atualização do banco dessa forma:

```
python ./manage.py  makemigrations

python ./manage.py migrate
```


## ⚙️ Descrição das funções para entendimento da logica do sistema

Função: home(request)
        Feature: Página inicial
            Cenário: Acessar a página inicial
                Dado que o usuário acessa o site
                Quando ele não especifica nenhuma URL
                Então a página inicial é exibida

Função: lista_vagas(request)
    Feature: Listagem de vagas
        Cenário: Visualizar a lista de vagas
            Dado que existem vagas cadastradas
            Quando o usuário acessa a página de listagem de vagas
            Então todas as vagas são mostradas para o usuário

Função: visualizar_candidatos(request, vaga_id)
    Feature: Visualizar candidatos de uma vaga
        Cenário: Acessar a lista de candidatos de uma vaga
            Dado que existem candidatos para uma vaga
            Quando o usuário acessa a página de visualização de candidatos para essa vaga
            Então todos os candidatos são mostrados para o usuário

Função: deletar_vaga(request, vaga_id)
    Feature: Deletar vaga
        Cenário: Deletar uma vaga existente
            Dado que existe uma vaga
            Quando o usuário solicita para deletar essa vaga
            Então a vaga é deletada e o usuário é redirecionado para a lista de vagas

Função: login_empresa(request)
    Feature: Login de empresa
        Cenário: Fazer login como empresa
            Dado que a empresa está registrada no sistema
            Quando a empresa fornece seu nome de usuário e senha corretos
            Então a empresa é logada e redirecionada para a página após o cadastro

Função: login_candidato(request)
    Feature: Login de candidato
        Cenário: Fazer login como candidato
            Dado que o candidato está registrado no sistema
            Quando o candidato fornece seu nome de usuário e senha corretos
            Então o candidato é logado e redirecionado para a página após o cadastro
            
Função: cadastro_candidato_view(request)
        Feature: Cadastro de candidato
            Cenário: Registrar um novo candidato
                Dado que o candidato não está registrado
                Quando o candidato fornece informações válidas de registro
                Então o candidato é registrado e redirecionado para a página de login de candidato

Função: cadastro_empresa_view(request)
    Feature: Cadastro de empresa
        Cenário: Registrar uma nova empresa
            Dado que a empresa não está registrada
            Quando a empresa fornece informações válidas de registro
            Então a empresa é registrada e redirecionada para a página de login de empresa

Função: custom_logout(request)
    Feature: Logout
        Cenário: Logout de um usuário logado
            Dado que o usuário está logado
            Quando o usuário solicita para fazer logout

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Django](https://docs.djangoproject.com/en/4.2/) - O framework web usado
* [Python](https://docs.python.org/3/) - Gerente de Dependência
* [SQLite3](https://www.sqlite.org/docs.html) - Banco de dados
* [Chartsjs](https://www.chartjs.org/docs/latest/) - Graficos
* [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) - Framework para estilização Web

## ✒️ Autores

@Mvrix - Me - https://www.linkedin.com/in/mvrix/

* **Mvrix** - *Meu portifolio completo* - [Mario](https://github.com/mvrix)

## 📄 Licença

Este projeto está sob a licença Django codigo aberto - veja o arquivo [LICENSE.md](https://docs.djangoproject.com/pt-br/4.2/faq/general/) para detalhes.

## 🎁 Expressões de gratidão!

* Foi um aprendizado muito rapido e muito fluido, amei cada dia de trabalho 📢;
* A organização foi feita através de um Kanban que fiz no Trello para não me perder ao longo do processo;
* Agradeço imensamente a JobConvo pela oportunidade e que eu atinja as expectativas 🫂;



---
⌨️ com ❤️ por [Mario](https://github.com/mvrix) 😊
