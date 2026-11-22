# Roteiro de prática e apresentação

Objetivo: que Lorena consiga demonstrar decisões e executar as ferramentas, sem depender de decorar o README.

1. Explicar o problema profissional em 60 segundos: demanda imprevista por unidade e atrasos do fornecedor são fenômenos distintos; ambos pressionam planejamento. Não afirmar que um causou o outro sem dados.
2. Abrir o CSV bruto e localizar a quantidade negativa, a referência U99 e a duplicata. Prever o que o pipeline fará; depois conferir `reports/qualidade.csv`.
3. Abrir o banco `data/processed/compras.sqlite` no DB Browser for SQLite ou outra ferramenta compatível. Executar:

```sql
SELECT unidade_id, SUM(planejado) planejado, SUM(solicitado) solicitado,
       SUM(excesso_unidades) excesso_local
FROM vw_demanda
GROUP BY unidade_id
ORDER BY excesso_local DESC;
```

4. Adicionar filtro de item antes de GROUP BY e explicar como o resultado mudou. Salvar a consulta executada em um novo arquivo e registrar os resultados com palavras próprias.
5. Executar a consulta abaixo; explicar por que AF com duas parcelas aparece somente uma vez:

```sql
SELECT af_item_id, quantidade, entregue, pendente, data_limite,
       data_conclusao, atraso_dias_corridos, situacao
FROM vw_entregas
WHERE af_item_id IN ('AF002','AF003','AF005');
```

6. Explicar por que a unidade não pode filtrar o recebimento se não temos alocação entre AF e unidade. Apontar essa limitação é parte da interpretação correta do modelo.
7. Seguir a montagem em `powerbi/README.md`. Conferir totais e executar a atualização demonstrativa. Só registrar evidências reais depois de fazê-las.
8. Demonstrar um caso de prazo: AF em 02/11, 15 dias corridos, início excluído, vencimento em 17/11 no calendário fictício. Repetir com dias úteis e explicar por que a cláusula importa.

## Como descrever o projeto enquanto está em preparação

“Estou desenvolvendo um estudo de compras e ressuprimento inspirado na minha experiência na assistência farmacêutica. Defini o problema operacional e as regras iniciais; o desenvolvimento tem apoio de IA. Estou revisando a execução em SQL e a implementação do relatório no Power BI.”

Depois de executar, substituir apenas as etapas efetivamente concluídas por descrições concretas. Não apresentar projeto assistido como experiência profissional de analista nem afirmar Power BI concluído antes da validação prática.
