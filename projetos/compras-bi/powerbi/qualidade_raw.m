// Exercício independente no Editor Avançado. PastaRaw é um parâmetro Texto
// apontando para data/raw. Não carregar esta tabela no modelo analítico:
// ela é uma demonstração parcial; quarentena completa é feita no Python.
let
    Fonte = Csv.Document(File.Contents(PastaRaw & "/demandas.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    SemDuplicatasExatas = Table.Distinct(Cabecalhos),
    ChavesPadronizadas = Table.TransformColumns(SemDuplicatasExatas,
        {{"unidade_id", each Text.Upper(Text.Trim(_)), type text},
         {"item_id", each Text.Upper(Text.Trim(_)), type text}}),
    Tipos = Table.TransformColumnTypes(ChavesPadronizadas,
        {{"competencia", type date}, {"planejado", Int64.Type}, {"solicitado", Int64.Type}}, "en-US"),
    Sinalizacao = Table.AddColumn(Tipos, "qualidade_quantidade",
        each if [planejado] < 0 or [solicitado] < 0 then "revisar" else "ok", type text)
in
    Sinalizacao
