-- CREATE MATERIALIZED VIEW ...
DROP MATERIALIZED VIEW IF EXISTS historial_paciente;

CREATE MATERIALIZED VIEW historial_paciente AS
SELECT 
    consulta.id,
    consulta.ssn,
    consulta.nif,
    consulta.nome,
    consulta.data,
    EXTRACT(YEAR FROM consulta.data) AS ano,
    EXTRACT(MONTH FROM consulta.data) AS mes,
    EXTRACT(DAY FROM consulta.data) AS dia_do_mes,
    SUBSTRING(clinica.morada FROM '[0-9]{4}-[0-9]{3} (.*)') AS localidade,
    medico.especialidade,
    'observacao' AS tipo,
    observacao.parametro AS chave,
    observacao.valor AS valor
FROM 
    consulta
JOIN 
    clinica ON consulta.nome = clinica.nome
JOIN 
    medico ON consulta.nif = medico.nif
JOIN 
    observacao ON consulta.id = observacao.id

UNION ALL

SELECT 
    consulta.id,
    consulta.ssn,
    consulta.nif,
    consulta.nome,
    consulta.data,
    EXTRACT(YEAR FROM consulta.data) AS ano,
    EXTRACT(MONTH FROM consulta.data) AS mes,
    EXTRACT(DAY FROM consulta.data) AS dia_do_mes,
    SUBSTRING(clinica.morada FROM '[0-9]{4}-[0-9]{3} (.*)') AS localidade,
    medico.especialidade,
    'receita' AS tipo,
    receita.medicamento AS chave,
    receita.quantidade AS valor
FROM 
    consulta
JOIN 
    clinica ON consulta.nome = clinica.nome
JOIN 
    medico ON consulta.nif = medico.nif
JOIN 
    receita ON consulta.codigo_sns = receita.codigo_sns;