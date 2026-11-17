# Publicação da demonstração acadêmica

## Render

1. Após o CI da branch `feat/solicitacoes-escolares` passar, entre no [painel do Render](https://dashboard.render.com/) e conecte o repositório GitHub.
2. Em **New → Blueprint**, selecione o repositório, a branch `feat/solicitacoes-escolares` e o arquivo `render.yaml`. Antes de aplicar, confira se o serviço web e o banco estão no plano **Free**.
3. O Blueprint gera a chave do Django e vincula a URL interna do PostgreSQL. O build instala as dependências e roda `collectstatic`. A inicialização aplica as migrações e inicia Gunicorn na porta fornecida pelo Render. WhiteNoise entrega os recursos estáticos.
4. Quando o deploy estiver ativo, abra a URL HTTPS fornecida no painel. Verifique a página inicial, `/solicitar/`, o redirecionamento de `/admin/` para o login e o HTTP 200 de `/health/`. Envie um pedido fictício pelo formulário e confira o recebimento pendente. O deploy automático está desligado. Para atualizar, espere o CI e selecione **Manual Deploy → Deploy latest commit**.
5. Para criar a conta administrativa em um serviço com Shell, execute `python manage.py createsuperuser` no Shell. No plano gratuito, o Shell não está disponível. Se precisar da conta para a demonstração, use um PostgreSQL separado com acesso administrativo autorizado ou crie a conta no banco do Render de um IP autorizado temporariamente conforme a documentação oficial. Use TLS, mantenha a URL externa e a senha só no ambiente local e remova a regra de acesso externo ao terminar. Nunca coloque credenciais no Blueprint.

O serviço web gratuito pode suspender após 15 minutos sem tráfego e levar cerca de um minuto para voltar. O disco do serviço é temporário. As solicitações ficam no PostgreSQL, que no plano gratuito expira em 30 dias e não inclui backups. Use dados fictícios e trate a instância gratuita como demonstração temporária.

[Guia Django no Render](https://render.com/docs/deploy-django) · [Planos gratuitos](https://render.com/docs/free) · [Conexões PostgreSQL](https://render.com/docs/postgresql-creating-connecting)

## Monitor externo

Com a URL pública funcionando, entre no UptimeRobot e crie um monitor do tipo HTTP(s) chamado **Casa Ateliê Jeff Alan**, apontando para a URL HTTPS real seguida de `/health/`. Se disponível no plano, escolha intervalo de 5 minutos e verifique o intervalo salvo. A rota retorna 200 quando a consulta `SELECT 1` funciona e 503 quando falha. Confira no painel a política real para erros HTTP e timeout, o estado registrado após a primeira checagem e o contato de alerta habilitado, se houver. Registre só o que for confirmado no painel.

Sem conta de monitoramento, um workflow agendado poderia verificar HTTPS e falhar se a resposta não for 200 ou estourar o timeout. O agendamento depende de a configuração estar na branch padrão, pode sofrer atrasos e só envia notificações conforme as preferências da conta. A checagem interna do Render, declarada no Blueprint, serve ao ciclo de vida do serviço e é distinta de um monitor público externo.

## Evidências

- No navegador, abra a página inicial pelo endereço público e pressione **Win + Shift + S**. Use a captura de janela e selecione a janela do navegador, com a barra de endereço inteira. Salve o arquivo.
- Faça um envio fictício e capture a confirmação pendente na URL pública.
- Com o primeiro resultado do monitor concluído, capture a tela com endereço consultado e estado. Ocultar áreas com credenciais ou dados pessoais ao selecionar a captura.
