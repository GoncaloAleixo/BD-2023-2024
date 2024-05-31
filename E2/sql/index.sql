--(1)
-- CREATE INDEX ...
-- Índice na coluna ssn da tabela consulta
CREATE INDEX idx_consulta_ssn ON consulta (ssn);

-- Índice na coluna id da tabela observacao
CREATE INDEX idx_observacao_id ON observacao (id);

-- Índice composto nas colunas parametro e valor da tabela observacao
CREATE INDEX idx_observacao_parametro_valor ON observacao (parametro, valor);

--(2)
-- CREATE INDEX ...
-- Índice na coluna nif da tabela consulta
CREATE INDEX idx_consulta_nif ON consulta (nif);

-- Índice na coluna codigo_sns da tabela receita
CREATE INDEX idx_receita_codigo_sns ON receita (codigo_sns);

-- Índice na coluna data da tabela consulta
CREATE INDEX idx_consulta_data ON consulta (data);