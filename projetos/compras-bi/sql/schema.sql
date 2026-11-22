PRAGMA foreign_keys = ON;
CREATE TABLE unidades (unidade_id TEXT PRIMARY KEY, unidade TEXT NOT NULL);
CREATE TABLE itens (item_id TEXT PRIMARY KEY, item TEXT NOT NULL, unidade_medida TEXT NOT NULL);
CREATE TABLE fornecedores (fornecedor_id TEXT PRIMARY KEY, fornecedor TEXT NOT NULL);
CREATE TABLE contratos (
 contrato_id TEXT PRIMARY KEY, fornecedor_id TEXT REFERENCES fornecedores,
 prazo_dias INTEGER NOT NULL CHECK(prazo_dias>0), tipo_dias TEXT,
 marco TEXT NOT NULL, regra_validada INTEGER CHECK(regra_validada IN (0,1)),
 ajustar_vencimento INTEGER CHECK(ajustar_vencimento IN (0,1)), fundamento TEXT
);
CREATE TABLE demandas (
 demanda_id TEXT PRIMARY KEY, competencia TEXT NOT NULL,
 unidade_id TEXT REFERENCES unidades, item_id TEXT REFERENCES itens,
 planejado INTEGER CHECK(planejado>=0), solicitado INTEGER CHECK(solicitado>=0),
 UNIQUE(competencia,unidade_id,item_id)
);
CREATE TABLE af_itens (
 af_item_id TEXT PRIMARY KEY, contrato_id TEXT REFERENCES contratos,
 item_id TEXT REFERENCES itens, data_envio TEXT NOT NULL,
 quantidade INTEGER CHECK(quantidade>0), preco_centavos INTEGER CHECK(preco_centavos>=0),
 data_limite TEXT
);
CREATE TABLE entregas (
 entrega_id TEXT PRIMARY KEY, af_item_id TEXT REFERENCES af_itens,
 data_entrega TEXT NOT NULL, quantidade INTEGER CHECK(quantidade>0)
);
CREATE TABLE parametros (data_corte TEXT NOT NULL);
