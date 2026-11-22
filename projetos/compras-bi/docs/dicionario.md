# Grão, dados e indicadores

Todos os nomes, contratos, autorizações e valores são fictícios. Não há pacientes, fornecedores reais ou dados internos da prefeitura.

| Arquivo/tabela | Grão e regra |
| --- | --- |
| unidades / itens / fornecedores | Uma linha por identificador; dimensão cadastral |
| contratos | Um contrato por fornecedor fictício; prazo, tipo de dias, marco e validação da regra |
| calendario | Data sem expediente no órgão fictício; complemento aos fins de semana |
| demandas | Unidade × item × competência mensal; chave de negócio única além de demanda_id |
| af_itens | Uma linha de medicamento por autorização; af_item_id é a chave, não o número de um contrato |
| entregas | Evento de entrega por AF-item; permite várias parcelas |
| vw_demanda | Mesmo grão da demanda; desvios absoluto/percentual e excesso positivo |
| vw_entregas | Mesmo grão da AF-item, após agregar entregas; saldo e situação no corte |
| vw_fornecedores | Agregação de AF-itens por fornecedor |

`planejado` representa quantidade mensal planejada; `solicitado`, demanda registrada pelas unidades. Nenhum deles equivale automaticamente a consumo atendido. `quantidade` da AF representa pedido ao fornecedor; `entregue` soma parcelas até o corte; `pendente = quantidade - entregue`. Quantidades de itens distintos são contagens logísticas, não doses equivalentes ou medida de benefício clínico. Comparações operacionais devem permitir filtrar por item.

`preco_centavos` é preço unitário inteiro; `valor_pendente_centavos = pendente * preco_centavos`. Valor pendente é saldo de fornecimento ao preço da amostra, não prejuízo, dívida liquidada ou despesa efetiva.

`desvio_pct` é nulo quando planejado=0 (denominador indefinido); não preencher com zero. `excesso_unidades = max(solicitado - planejado, 0)` no grão local. Pontualidade não inclui pedidos ainda abertos; por isso deve ser lida junto das pendências vencidas.

`atraso_dias_corridos` conta dias após data_limite até conclusão integral ou corte. Saldo parcial não encerra o prazo do restante. Se a regra não está validada, prazo/atraso são nulos e a situação é `regra_pendente`. O painel não infere falta de estoque: sem inventário e saídas diárias, a análise mostra pressão sobre abastecimento, não ruptura comprovada ou relação causal.

## Qualidade e rastreabilidade

Duplicata exata: manter uma cópia e registrar remoção. Mesmo ID com conteúdos diferentes: rejeitar todas as versões para revisão, sem escolher uma arbitrária. Demanda no mesmo grão com IDs diferentes também vai para revisão. Espaços e caixa das referências são normalizados com registro. Quantidades negativas, referência ausente, data inválida/futura e entrega anterior à AF são rejeitadas. Entregas acima do total do pedido são rejeitadas como conjunto por AF.

`reports/qualidade.csv` contém fonte, linha física (0 para validação de conjunto), chave, ação e motivo. `reports/execucao.json` concilia entrada = aceitos + duplicatas + rejeitados; uma ação de padronização não remove linha e não entra nessa soma. Hashes SHA-256 identificam os arquivos de entrada usados. O banco é reconstruído a cada execução, de modo idempotente.

A aplicação foi desenhada para o esquema demonstrativo. Mudanças de layout ou cadastros inválidos devem interromper a carga; a adaptação a sistemas reais não foi implementada.
