# Plano de validação externa

Status: planejado. Não há resultados, consentimentos ou rodadas realizadas registrados neste documento.

## Participação e privacidade
Convidar uma professora ou coordenadora relacionada ao contexto escolar. Confirmar disponibilidade e consentimento antes do teste. Manter identificação pessoal e registro de concordância fora do repositório público, salvo autorização específica. Usar apenas dados fictícios.

## Evolução entre experiências
O teste do protótipo estático observa interpretação: a participante aponta ações e simula o preenchimento verbalmente. Não comprova funcionamento.
Na EP III, realizar pelo menos duas rodadas com o MVP funcional: primeira avaliação, registro de feedback, correções reais no código e segunda avaliação das mudanças.

## Tarefas
1. Localizar como solicitar atividade escolar a partir da página inicial. Esperado: identificar a ação de solicitação. Avalia RF01, reconhecimento de RF02 e clareza visual de RNF04.
2. Preparar e enviar pedido fictício. Esperado no MVP funcional: preencher seis campos, enviar e receber resultado após gravação. Avalia RF03, minimização de dados e clareza de instruções. A persistência será também verificada tecnicamente.
3. Interpretar o resultado e voltar ao início. Esperado: explicar que recebido não significa confirmado e identificar próximo passo por texto, sem depender de cor. Avalia RF03 e RNF04.

## Cenário
Escola Exemplo do Bairro; Pessoa de Teste; educador@example.org; visita educativa; manhã em março de 2027 a combinar; 25 participantes.

## Condução
Sessão individual moderada de 15 a 20 minutos. Registrar versão, dispositivo, navegador e condições. Ler objetivos sem ensinar os controles. Repetição literal do enunciado não conta como ajuda; orientação sobre como resolver conta. Após pedido de ajuda ou 60 segundos sem progresso, permitir orientação neutra e registrar.
No protótipo estático, a troca de tela pelo moderador não conta como ajuda. No MVP funcional, a participante executa as ações diretamente.

## Registro por rodada
- Data real e versão/commit avaliado.
- Resultado por tarefa: independente, com ajuda ou falha.
- Tempo, erros, autocorreções e intervenções.
- Comentário literal autorizado, separado de interpretação do moderador.
- Nota de facilidade por tarefa e satisfação ao final.
- Problema identificado, prioridade, alteração proposta e commit que a implementou.

## Segunda rodada
Repetir as tarefas afetadas e conferir regressões no percurso completo. Identificar aprendizado decorrente da primeira sessão. Preservar resultados originais. Nunca preencher feedbacks, tempos ou aprovação sem observação real.
