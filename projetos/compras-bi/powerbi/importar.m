// Consulta em branco chamada fnCSV. PastaBase é um parâmetro Texto com
// caminho COMPLETO até data/processed (sem barra final).
(nome as text, tipos as list) as table =>
let
    Fonte = Csv.Document(File.Contents(PastaBase & "/" & nome & ".csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    Nulos = Table.ReplaceValue(Cabecalhos, "", null, Replacer.ReplaceValue, Table.ColumnNames(Cabecalhos)),
    Tipado = Table.TransformColumnTypes(Nulos, tipos, "en-US")
in Tipado

// Cada expressão abaixo deve ser uma NOVA consulta com o nome indicado.
// DimUnidade
// fnCSV("unidades", {{"unidade_id", type text}, {"unidade", type text}})
// DimItem
// fnCSV("itens", {{"item_id", type text}, {"item", type text}, {"unidade_medida", type text}})
// DimFornecedor
// fnCSV("fornecedores", {{"fornecedor_id", type text}, {"fornecedor", type text}})
// FatoDemanda
// fnCSV("vw_demanda", {{"demanda_id", type text}, {"competencia", type date}, {"unidade_id", type text}, {"item_id", type text}, {"planejado", Int64.Type}, {"solicitado", Int64.Type}, {"desvio_unidades", Int64.Type}, {"desvio_pct", type number}, {"excesso_unidades", Int64.Type}})
// FatoAF
// fnCSV("vw_entregas", {{"af_item_id", type text}, {"contrato_id", type text}, {"item_id", type text}, {"data_envio", type date}, {"quantidade", Int64.Type}, {"preco_centavos", Int64.Type}, {"data_limite", type date}, {"fornecedor_id", type text}, {"tipo_dias", type text}, {"entregue", Int64.Type}, {"pendente", Int64.Type}, {"data_conclusao", type date}, {"data_corte", type date}, {"valor_pendente_centavos", Int64.Type}, {"atraso_dias_corridos", Int64.Type}, {"situacao", type text}})
