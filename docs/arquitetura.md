# Arquitetura e dados

Status: decisões de projeto, ainda não evidências de execução.

## Organização
Aplicação monolítica em camadas lógicas:
- Apresentação: templates Django, HTML e CSS.
- Aplicação: views coordenam requisições; serviços concentram atribuição e transições dos pedidos.
- Persistência: models e ORM Django, conectados ao PostgreSQL pelo Psycopg.

Python 3.13 e Django 5.2 LTS são as versões-base previstas. Atualizações corretivas e versões exatas das dependências deverão ser registradas durante a implementação.

## Entidades
### Obra
Identificador automático; título (200), descrição, técnica opcional (150), ano opcional positivo, referência de imagem, texto alternativo (300), publicada (padrão falso), data de criação. Imagens ficam em armazenamento persistente; somente referências ficam no banco.

### SolicitacaoEscolar
Identificador automático; escola (200), nome de contato (150), e-mail, atividade (300), período pretendido (200), quantidade positiva, situação (pendente por padrão), responsável opcional e datas de criação/atualização.
Responsável é chave estrangeira para usuário administrativo: um usuário acompanha muitos pedidos; um pedido tem zero ou um responsável. Bloquear exclusão de usuário vinculado e preferir desativação.

### Usuário administrativo
Utilizar o modelo e permissões do Django. Identificador, username único, nome, hash de senha, conta ativa, acesso administrativo e datas de criação/login. Não criar cadastro público.

## Fluxo central
Formulário → validação no servidor → serviço de criação → gravação → confirmação de recebimento.
Se houver erro de validação, devolver campos e mensagens. Se houver falha de gravação, não apresentar sucesso.
Na administração: verificar permissão → consultar → assumir pedido → iniciar análise → confirmar ou recusar. O painel deve chamar as mesmas regras de aplicação.

## Segurança e implantação previstas
PBKDF2-HMAC-SHA256 via Django; HTTPS; sessões no servidor; CSRF; escape de saída; consultas parametrizadas; privilégios mínimos. Segredos externos ao repositório, DEBUG desativado e hosts explícitos em produção.
Limitação de login requer implementação adicional com contadores compartilhados. O cache em banco pode apoiar o MVP, devendo ser testado quanto à concorrência.
Desenvolvimento local; publicação Linux com servidor WSGI, PostgreSQL e arquivos persistentes. Custos, backups e limites do provedor ainda dependem de avaliação.

## Limitações
O protótipo visual não implementa banco, autorização ou regras. Nenhuma credencial, dado de estudantes ou contato real deverá entrar nas fixtures públicas.
