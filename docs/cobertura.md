# Medição local de cobertura — 17/11/2026

Código avaliado: 7418e66a32efa59c52440a7ee6e31e2ead83a707.
20 testes aprovados em 3,085 segundos. Cobertura de linhas: 130 de 139 instruções, 93,53% (94% arredondado).
Escopo: pacote solicitacoes. Excluídos tests.py e migrations. Não inclui templates, configuração ou código ainda não implementado. Não é cobertura de branches nem comprovação de qualidade completa.
Ambiente: Python 3.12.14, Django 5.2.19, SQLite em memória. Não é execução CI ou teste de concorrência PostgreSQL.

## Reprodução
Instale `python -m pip install -r requirements-dev.txt`. Configure as variáveis descritas em implementacao-inicial.md, incluindo USE_SQLITE=1 e DJANGO_DEBUG=1 para reproduzir esta execução local.
Execute:
```
python -m coverage run manage.py test --verbosity 2
python -m coverage report
```
O teste de falha de persistência gera intencionalmente um log de erro e deve terminar com aprovação.

## Linhas ainda não executadas
admin.py: 27-29, 41, 45, 49; services.py: 10; views.py: 22-23. Os testes de serviços cobrem transições, mas nem todas as ações administrativas e exceções são exercitadas pela interface.
