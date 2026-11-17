# Critérios de aceite e plano de qualidade

Status: metas e testes planejados; resultados pendentes.

## Validação do protótipo
| Dimensão | Métrica | Meta |
| --- | --- | --- |
| Usabilidade | Tarefas corretas sem orientação / 3 | 100%: três de três |
| Eficiência | Tempo da tarefa 2 de compreensão e simulação | Até 180 segundos |
| Satisfação | Escala de 1 (muito insatisfeita) a 5 (muito satisfeita) | Pelo menos 4 |

Cronometrar após leitura do enunciado até a ação correta. Dúvidas e releitura contam no tempo. Descontar apenas pausas técnicas documentadas. No protótipo, excluir tempo do moderador para trocar telas.
Pergunta de satisfação: “Considerando as três telas, qual é seu nível de satisfação com a clareza das informações e a facilidade para identificar o que fazer?”
A meta de 180 segundos foi definida para simulação estática. Antes da primeira rodada funcional, documentar sua adequação ao preenchimento real e congelar o protocolo; não alterar limites depois de observar resultados para obter aprovação.

## Decisão
Aceito: todas as metas atingidas, sem falha crítica.
Aceito com ajustes: metas atingidas, com melhorias pontuais sem bloqueio.
Revisão obrigatória: qualquer meta não atingida ou falha crítica, como confundir recebimento com reserva, não localizar o envio ou não compreender a situação por texto.
Não compensar falha de compreensão com velocidade ou satisfação. Preservar cada rodada e suas limitações; um participante não representa todo o público.

## Testes automatizados a implementar
- Unitários: campos obrigatórios, e-mail, quantidade positiva e transições permitidas.
- Integração: envio válido grava pendente; envio inválido não grava; falha de armazenamento não informa sucesso.
- Acesso: visitante e usuário sem permissão não consultam ou alteram pedidos.
- Administração: atribuição não muda situação; análise exige responsável; confirmação direta de pendente é rejeitada.
- Segurança: CSRF, escape de entrada na saída, sessão encerrada e limites de login.

## Integração contínua planejada
GitHub Actions deverá instalar dependências, preparar banco de teste, verificar configuração/migrações e executar testes e cobertura. Registrar execução real e seus resultados. Testes que falham devem impedir a conclusão bem-sucedida do pipeline.

## Revisão por Pull Request
Implementar funcionalidades em branch própria e abrir PR descrevendo problema, mudança e validação. Na autorrevisão, conferir permissões, regras, dados sensíveis, testes e instruções. Registrar correções reais encontradas. Os commits de documentação não substituem PR e testes de código.

## Evidências
Manter SHA, data, logs de testes, execução CI, capturas do sistema funcional e feedback anonimizado autorizado. Não publicar credenciais ou atribuir resultados ainda não obtidos.
