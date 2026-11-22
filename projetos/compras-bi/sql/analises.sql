-- SQLite 3.25+. Os recebimentos são agregados ANTES do JOIN para não
-- multiplicar a quantidade solicitada em AF com entregas parciais.
CREATE VIEW vw_demanda AS
SELECT d.*, solicitado-planejado AS desvio_unidades,
 CASE WHEN planejado=0 THEN NULL ELSE ROUND(100.0*(solicitado-planejado)/planejado,2) END AS desvio_pct,
 MAX(solicitado-planejado,0) AS excesso_unidades
FROM demandas d;

CREATE VIEW vw_entregas AS
WITH recebimentos AS (
 SELECT af_item_id, SUM(quantidade) entregue, MAX(data_entrega) ultima_entrega
 FROM entregas GROUP BY af_item_id
), base AS (
 SELECT a.*, c.fornecedor_id, c.tipo_dias, COALESCE(r.entregue,0) entregue,
 a.quantidade-COALESCE(r.entregue,0) pendente,
 CASE WHEN COALESCE(r.entregue,0)=a.quantidade THEN r.ultima_entrega END data_conclusao,
 p.data_corte
 FROM af_itens a JOIN contratos c USING(contrato_id)
 LEFT JOIN recebimentos r USING(af_item_id) CROSS JOIN parametros p
)
SELECT *, pendente*preco_centavos AS valor_pendente_centavos,
 CASE WHEN data_limite IS NULL THEN NULL
 ELSE MAX(CAST(julianday(COALESCE(data_conclusao,data_corte))-julianday(data_limite) AS INTEGER),0)
 END AS atraso_dias_corridos,
 CASE WHEN data_limite IS NULL THEN 'regra_pendente'
 WHEN pendente=0 AND data_conclusao<=data_limite THEN 'concluido_no_prazo'
 WHEN pendente=0 THEN 'concluido_com_atraso'
 WHEN data_corte>data_limite THEN 'pendente_vencido'
 ELSE 'pendente_no_prazo' END AS situacao
FROM base;

CREATE VIEW vw_fornecedores AS
SELECT fornecedor_id, COUNT(*) af_itens,
 SUM(quantidade) quantidade_pedida, SUM(entregue) quantidade_entregue,
 SUM(pendente) quantidade_pendente,
 SUM(CASE WHEN situacao='pendente_vencido' THEN 1 ELSE 0 END) pendencias_vencidas,
 SUM(CASE WHEN situacao='regra_pendente' THEN 1 ELSE 0 END) regras_pendentes,
 SUM(valor_pendente_centavos) valor_pendente_centavos,
 -- Denominador: somente AF-itens concluídas com prazo calculável.
 ROUND(100.0*SUM(CASE WHEN situacao='concluido_no_prazo' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN situacao IN ('concluido_no_prazo','concluido_com_atraso') THEN 1 ELSE 0 END),0),2) AS pontualidade_concluidos_pct
FROM vw_entregas GROUP BY fornecedor_id;

-- Consultas para entrevista (executar separadamente na base gerada):
-- SELECT unidade_id, SUM(excesso_unidades) excesso FROM vw_demanda
-- GROUP BY unidade_id ORDER BY excesso DESC;
-- SELECT af_item_id, pendente, atraso_dias_corridos FROM vw_entregas
-- WHERE situacao='pendente_vencido' ORDER BY atraso_dias_corridos DESC;
-- SELECT * FROM vw_fornecedores ORDER BY pontualidade_concluidos_pct;
