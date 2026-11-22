# Resultados da execução demonstrativa

Data de corte: **22/11/2026**. Dados inteiramente simulados. Resultado do pipeline Python/SQLite executado pelo assistente, não do Power BI nem de uma execução pessoal de Lorena.

| Conciliação | Resultado |
| --- | ---: |
| Demandas brutas | 203 |
| Demandas aceitas | 200 |
| Duplicatas exatas removidas | 1 |
| Demandas rejeitadas | 2 |
| AF-itens brutos | 52 |
| AF-itens aceitos | 50 |
| Versões de AF conflitantes rejeitadas | 2 |
| Eventos de entrega aceitos | 50 |
| Quantidade total pedida | 31.052 |
| Quantidade entregue | 21.900 |
| Quantidade pendente | 9.152 |
| Valor do saldo de fornecimento | R$ 4.390,01 |
| Planejado nas unidades | 25640 |
| Solicitado nas unidades | 31052 |
| Excesso somado por unidade/item/mês | 6306 |

31.052 = 21.900 + 9.152. Há 50 AF-itens e 50 eventos de entrega, mas a distribuição não é de um evento por pedido: algumas AF têm duas parcelas e outras nenhuma. A agregação prévia preserva o total pedido.

| Situação no corte | AF-itens |
| --- | ---: |
| concluido_com_atraso | 20 |
| concluido_no_prazo | 10 |
| pendente_vencido | 20 |

Há demanda acima do planejamento e saldos vencidos por construção da amostra; isso demonstra o método, não um achado sobre o município. Atraso de entrega não comprova ruptura sem saldo inicial e movimentações de estoque. O valor pendente não representa prejuízo.

Evidências: [log de qualidade](qualidade.csv), [totais e hashes de entrada](execucao.json), [testes executáveis](../tests/test_pipeline.py). Se alterar a amostra, regenerar e revisar este resumo; o JSON e os CSVs são as saídas automáticas de cada execução.
