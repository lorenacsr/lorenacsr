# Compras e ressuprimento de medicamentos

**SQL · qualidade de dados · ETL em Python · preparação de Power BI**

Projeto de portfólio em desenvolvimento, inspirado no problema identificado por **Lorena Reis** em sua atuação na assistência farmacêutica: demandas fora do planejado de diferentes unidades e atrasos no ressuprimento contratado. Amostra inteiramente simulada, sem dados da prefeitura ou pacientes.

**Estado verificável:** pipeline Python/SQLite executado e testado; consultas, exportações e relatório de conciliação disponíveis. Consultas Power Query e medidas DAX preparadas; montagem, execução e validação no Power BI por Lorena **pendentes**. Não há arquivo PBIX concluído nem alegação de experiência profissional em BI. [Participação e apoio de IA](docs/contribuicoes.md).

## Perguntas de negócio

- Quais unidades e medicamentos concentram demanda acima do planejamento mensal?
- Quais AF-itens continuam com saldo depois do vencimento contratual?
- Como comparar pontualidade de fornecedores sem esconder pedidos abertos?
- Que inconsistências precisam ser resolvidas antes de alimentar um painel?

## Evidências técnicas

| Competência | Onde conferir |
| --- | --- |
| SQL: JOIN, CTE, agregações, CASE, NULLIF e views | [Consultas](sql/analises.sql) e [modelo relacional](sql/schema.sql) |
| Limpeza, padronização, quarentena e rastreabilidade | [Pipeline](src/pipeline.py), [auditoria](reports/qualidade.csv) e [conciliação](reports/execucao.json) |
| Entregas parciais e validação dos totais | [Resultados executados](reports/resultados.md) e [testes](tests/test_pipeline.py) |
| Modelagem para BI e prevenção de dupla contagem | [Dicionário e grãos](docs/dicionario.md) |
| Importação, transformação e atualização Power BI | [Roteiro de execução](powerbi/README.md), [M](powerbi/importar.m), [transformação bruta M](powerbi/qualidade_raw.m) e [DAX](powerbi/medidas.dax); validação na ferramenta pendente |
| Regras de prazo fundamentadas | [Base legal, hipóteses e pendências](docs/base-legal.md) |

## Reproduzir sem instalar dependências

Requer Python 3.10+ com módulo sqlite3. No terminal, a partir da raiz deste projeto:

```bash
python src/pipeline.py run
python -m unittest discover -s tests -v
```

Os dados brutos já estão versionados. Para recriar exatamente a amostra com semente 42:

```bash
python src/pipeline.py generate
python src/pipeline.py run --data-corte 2026-11-22
```

`generate` sobrescreve a amostra bruta de demonstração; `run` mantém o bruto e recria as saídas. Não apontar o gerador para dados reais. CSVs tratados ficam em `data/processed`; o banco SQLite é gerado localmente e não versionado. Para consultar, abrir `data/processed/compras.sqlite` em ferramenta SQLite e executar os SELECTs ao final de `sql/analises.sql`. O arquivo de views completo é executado pelo pipeline, não deve ser reaplicado sobre views existentes.

## Fluxo e limites

Brutos CSV → validação e quarentena → modelo relacional SQLite → consultas SQL → CSVs analíticos → Power BI (etapa prática pendente). As entregas são agregadas antes do JOIN com AF, evitando duplicar quantidades quando há mais de uma parcela.

Os 15 dias foram informados por Lorena como regra do contrato de sua rotina, não como prazo geral da lei. Como a cláusula não foi lida, a amostra adota **contratos fictícios expressos em dias corridos** e calendário fictício; essa hipótese não resolve o contrato municipal. O modelo sinaliza regras desconhecidas, suporta dias úteis e não decide sanções.

Não há base suficiente para comprovar ruptura, responsabilização de fornecedor, prejuízo financeiro ou causalidade. A demanda é solicitação, não consumo efetivo. Todos os valores e nomes são sintéticos.

## Próximas etapas práticas

Seguir o [roteiro de SQL e interpretação](docs/roteiro-pratica.md), montar o PBIX, validar resultados e atualizar o [registro de contribuições](docs/contribuicoes.md) com evidências reais. A documentação separa decisões de Lorena, implementação assistida e tarefas ainda não realizadas.
