# Montagem e validação no Power BI Desktop

**Estado: preparado, ainda não executado nem validado no Power BI. Não há PBIX concluído neste projeto.** As consultas M e medidas DAX são ponto de partida para a etapa prática de Lorena. A prévia de resultados SQL não é um dashboard Power BI.

1. Em um computador Windows com Power BI Desktop, baixar o repositório e executar o pipeline conforme o README principal.
2. Em Transformar dados > Gerenciar parâmetros, criar `PastaBase` (Texto) com o caminho absoluto de `data/processed` e `PastaRaw` com o caminho de `data/raw`. Os caminhos são locais; não subir caminhos pessoais ou credenciais ao GitHub.
3. Criar uma consulta em branco, nomear `fnCSV` e colar a função de `importar.m` no Editor Avançado. Em novas consultas, colar as expressões comentadas no mesmo arquivo sem os `//`. Nomear exatamente como indicado. Conferir tipos, valores nulos e datas antes de carregar.
4. Criar relações **1 para muitos**, filtro em direção única da dimensão para o fato:

| Dimensão | Fato | Chave |
| --- | --- | --- |
| DimItem | FatoDemanda | item_id |
| DimItem | FatoAF | item_id |
| DimUnidade | FatoDemanda | unidade_id |
| DimFornecedor | FatoAF | fornecedor_id |

**Não relacionar FatoDemanda diretamente a FatoAF.** A demanda tem grão unidade × medicamento × mês. A AF tem grão item de autorização. Não existe alocação de AF por unidade neste conjunto; um filtro por unidade não deve sugerir que filtra entregas.

5. Criar cada medida de `medidas.dax` separadamente. Formatar Desvio Percentual e Pontualidade Concluidos como percentual; Valor Pendente como moeda BRL. Centavos são inteiros na origem para preservar conciliação.
6. Página **Demanda**: filtros por unidade, item e competência; cartões Planejado, Solicitado e Desvio Percentual; colunas agrupadas por mês (planejado × solicitado); barras de Excesso Local por unidade. Excesso Local soma somente desvios positivos de cada unidade/item/mês; não equivale ao desvio líquido consolidado.
7. Página **Entregas**: filtros por fornecedor, item e situação; cartões Saldo Pendente, Valor Pendente, AF Itens Vencidos e Pontualidade Concluidos; tabela com af_item_id, data_envio, data_limite, entregue, pendente, atraso_dias_corridos e situacao. A pontualidade tem como denominador apenas AF-itens concluídos com regra definida; mostrar pendências vencidas ao lado para evitar viés.
8. Página **Qualidade**: importar `reports/qualidade.csv`, visualizar ações por fonte e motivo; mostrar Regras Pendentes. Executar `qualidade_raw.m` como exercício separado para inspecionar as etapas de transformação, sem alimentar as medidas principais com uma tabela parcialmente tratada.
9. Conferir os totais contra `reports/resultados.md` **sem filtros**. `Conciliacao Quantidades` deve resultar em zero. Com filtros comuns de item/fornecedor na página de entregas, a igualdade também deve permanecer zero.
10. Salvar PBIX. Registrar capturas reais das páginas, do modelo e da validação. Somente depois disso marcar a etapa como concluída em `docs/contribuicoes.md`.

## Exercício de atualização real

Fazer uma cópia do projeto antes da alteração. No CSV bruto de demandas, localizar D0001 e suas duas cópias idênticas: alterar `solicitado` de ambas para o mesmo valor novo, preservando a duplicata exata como teste. Reexecutar `python src/pipeline.py run`; em seguida clicar **Atualizar** no Desktop. O total solicitado deve mudar exatamente pela diferença inserida, sem duplicação. Conferir o novo `reports/execucao.json` e atualizar o registro de evidências. Voltar à amostra original com `generate` e `run` quando desejar.

Os CSVs fornecidos permitem importação local. Atualização agendada no serviço exige configuração própria de acesso/gateway quando aplicável; não foi implantada. A data de corte é fixa para reprodutibilidade: para outra análise, reexecutar o pipeline com `--data-corte AAAA-MM-DD`. O relatório não se atualiza automaticamente ao abrir o calendário.

## Referências oficiais

- [Conector Texto/CSV](https://learn.microsoft.com/en-us/power-query/connectors/text-csv)
- [Criar medidas DAX](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tutorial-create-measures)
- [Atualização de dados](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data)
