# Requisitos do MVP — Casa Ateliê Jeff Alan

Status: especificação planejada. Este documento não comprova implementação.

## Objetivo e público
Apresentar o artista e o espaço e organizar solicitações de atividades escolares. Usuários diretos: educadores e responsável administrativo. Estudantes não terão contas nem dados individuais coletados.

## Requisitos funcionais
| ID | Prioridade | Comportamento e aceite |
| --- | --- | --- |
| RF01 | Obrigatório | Apresentar artista, espaço e orientações escolares, com acesso ao catálogo e à solicitação, sem login. |
| RF02 | Obrigatório | Exibir somente obras publicadas, com imagem, título e descrição; mostrar mensagem quando o catálogo estiver vazio. |
| RF03 | Obrigatório | Receber escola, nome, e-mail, atividade, período pretendido e quantidade de participantes. Validar campos e gravar como pendente. Informar sucesso somente após a gravação, esclarecendo que não há reserva. |
| RF04 | Obrigatório | Permitir consulta da lista e dos detalhes dos pedidos apenas a contas ativas com permissão, inclusive por URL direta. Ordenar do mais recente para o mais antigo. |
| RF05 | Obrigatório | Permitir que administrador autorizado assuma pedido sem responsável. Atribuir sua conta sem alterar automaticamente a situação. |
| RF06 | Obrigatório | Permitir pendente → em análise → confirmada ou recusada. Exigir responsável antes da análise; rejeitar outras transições; registrar atualização. |
| RF07 | Desejável | Filtrar lista administrativa por situação e permitir remover o filtro sem alterar registros. |

## Regras de validação
Todos os campos do pedido são obrigatórios. E-mail deve ter formato válido e participantes deve ser inteiro positivo. Situação e responsável não podem ser definidos pelo formulário público. Escola e e-mail não são únicos: um contato pode enviar vários pedidos.

## Dependências e incrementos
Primeiro incremento: apresentação e catálogo. Segundo: envio e acompanhamento administrativo completo. Desenvolver a consulta com dados de teste e liberar o formulário para uso real somente quando o acompanhamento funcionar.

## Fora do escopo
Venda de obras, chat, pagamento, agendamento automático e histórico completo de mudanças. A confirmação exige avaliação humana e contato com a escola.

## Qualidade planejada
Autenticação administrativa, proteção de dados, acessibilidade e desempenho devem ser implementados e testados. Capturas estáticas não comprovam esses controles.
