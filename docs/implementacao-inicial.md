# Primeira entrega funcional: solicitações

## Escopo entregue
Formulário público em /solicitar/, persistência, resultado após gravação e administração em /admin/. Serviços centralizam atribuição e transições. A área administrativa usa ações e campos somente leitura para evitar alteração direta que ignore serviços.

## Execução local
Requer Python 3.13 recomendado (também testado com Python 3.12). Instale dependências: `python -m pip install -r requirements.txt`.
Defina DJANGO_SECRET_KEY com um valor aleatório local, DJANGO_DEBUG=1 e as variáveis PostgreSQL listadas em .env.example no terminal. O arquivo .env não é carregado automaticamente. Não versione credenciais.
Execute `python manage.py migrate`, `python manage.py createsuperuser` e `python manage.py runserver`.
Acesse http://127.0.0.1:8000/solicitar/ e http://127.0.0.1:8000/admin/.
Crie usuário staff de operação com permissões view e change de SolicitacaoEscolar. Use superusuário apenas para configuração.

## Testes
`python manage.py test` e `python manage.py makemigrations --check --dry-run`.
Para teste local sem PostgreSQL, definir USE_SQLITE=1 junto de DJANGO_DEBUG=1. Este opt-in não altera a escolha de PostgreSQL do projeto e não comprova bloqueios concorrentes deste banco.

## Limitações explícitas
Entrega incremental, ainda não MVP completo. Catálogo e apresentação, visual final, limitação de tentativas de login, CSP, testes reais de acessibilidade/desempenho, implantação e pipeline CI permanecem pendentes. Não publicar para uso real antes de completar controles. A expiração de 30 minutos do cookie está configurada; não é declarada como teste de política absoluta de sessão para todos os casos.
O banco de testes é isolado. Nenhuma rodada com participante externo foi realizada por este código. A confirmação administrativa depende de avaliação e contato humanos.
