-- (1)
-- SELECT ...
WITH ortopedia_observacoes AS (
    SELECT 
        hp.ssn,
        hp.chave,
        hp.data,
        LAG(hp.data) OVER (PARTITION BY hp.ssn, hp.chave ORDER BY hp.data) AS data_anterior
    FROM historial_paciente hp
    JOIN medico m ON hp.nif = m.nif
    WHERE hp.tipo = 'observacao'
        AND hp.valor IS NULL
        AND m.especialidade = 'ortopedia'
),
intervalos AS (
    SELECT
        ssn,
        chave,
        data,
        data_anterior,
        COALESCE(EXTRACT(EPOCH FROM (data::timestamp - data_anterior::timestamp)) / 86400, 0) AS intervalo_dias
    FROM ortopedia_observacoes
),
max_intervalos AS (
    SELECT
        ssn,
        MAX(intervalo_dias) AS max_intervalo
    FROM intervalos
    GROUP BY ssn
),
max_intervalo_global AS (
    SELECT
        MAX(max_intervalo) AS max_intervalo
    FROM max_intervalos
)
SELECT
    p.nome AS nome_paciente,
    mi.ssn,
    ROUND(mi.max_intervalo, 2) AS intervalo_temporal
FROM max_intervalos mi
JOIN paciente p ON mi.ssn = p.ssn
JOIN max_intervalo_global mg ON mi.max_intervalo = mg.max_intervalo;

-- (2)
-- SELECT ...
WITH cardiologia_consultas AS (
    SELECT
        c.id AS consulta_id,
        c.ssn,
        c.data,
        r.medicamento
    FROM
        consulta c
    JOIN
        medico m ON c.nif = m.nif
    JOIN
        receita r ON c.codigo_sns = r.codigo_sns
    WHERE
        m.especialidade = 'cardiologia'
        AND c.data >= (CURRENT_DATE - INTERVAL '1 year')
),
receitas_mensais AS (
    SELECT
        ssn,
        medicamento,
        DATE_TRUNC('month', data) AS mes
    FROM
        cardiologia_consultas
    GROUP BY
        ssn, medicamento, DATE_TRUNC('month', data)
),
medicamentos_contagem AS (
    SELECT
        ssn,
        medicamento,
        COUNT(DISTINCT mes) AS meses_receitado
    FROM
        receitas_mensais
    GROUP BY
        ssn, medicamento
),
medicamentos_cronicos AS (
    SELECT
        medicamento
    FROM
        medicamentos_contagem
    WHERE
        meses_receitado = 12
)
SELECT DISTINCT
    medicamento
FROM
    medicamentos_cronicos;

-- (3)
-- SELECT ...
SELECT
    r.medicamento,
    CASE WHEN GROUPING(c.localidade) = 1 THEN 'Total'
         ELSE c.localidade END AS localidade,
    CASE WHEN GROUPING(cl.nome) = 1 THEN 'Total'
         ELSE cl.nome END AS clinica,
    CASE WHEN GROUPING(m.especialidade) = 1 THEN 'Total'
         ELSE m.especialidade END AS especialidade,
    CASE WHEN GROUPING(m.nome) = 1 THEN 'Total'
         ELSE m.nome END AS nome_medico,
    CASE WHEN GROUPING(EXTRACT(MONTH FROM co.data)) = 1 THEN 'Total'
         ELSE TO_CHAR(EXTRACT(MONTH FROM co.data), 'FM00') END AS mes,
    CASE WHEN GROUPING(EXTRACT(DAY FROM co.data)) = 1 THEN 'Total'
         ELSE TO_CHAR(EXTRACT(DAY FROM co.data), 'FM00') END AS dia_do_mes,
    SUM(r.quantidade) AS quantidade_total
FROM
    receita r
JOIN
    consulta co ON r.codigo_sns = co.codigo_sns
JOIN
    clinica cl ON co.nome = cl.nome
JOIN
    medico m ON co.nif = m.nif
JOIN
    (SELECT DISTINCT
         SUBSTRING(cl.morada FROM '[0-9]{4}-[0-9]{3}') || ', ' || SUBSTRING(cl.morada FROM '[A-Za-z\s]+$') AS localidade,
         cl.nome
     FROM clinica cl) c ON c.nome = cl.nome
WHERE
    EXTRACT(YEAR FROM co.data) = 2023
GROUP BY
    GROUPING SETS (
        (r.medicamento, c.localidade, cl.nome, m.especialidade, m.nome, EXTRACT(MONTH FROM co.data), EXTRACT(DAY FROM co.data)),
        (r.medicamento, c.localidade, cl.nome, m.especialidade, m.nome, EXTRACT(MONTH FROM co.data)),
        (r.medicamento, c.localidade, cl.nome, m.especialidade, m.nome),
        (r.medicamento, c.localidade, cl.nome, m.especialidade),
        (r.medicamento, c.localidade, cl.nome),
        (r.medicamento, c.localidade),
        (r.medicamento),
        ()
    )
ORDER BY
    r.medicamento, c.localidade, cl.nome, m.especialidade, m.nome, mes, dia_do_mes;

-- (4)
-- SELECT ...
SELECT
    CASE WHEN GROUPING(m.especialidade) = 1 THEN 'Total'
         ELSE m.especialidade END AS especialidade,
    CASE WHEN GROUPING(m.nome) = 1 THEN 'Total'
         ELSE m.nome END AS medico,
    CASE WHEN GROUPING(cl.nome) = 1 THEN 'Total'
         ELSE cl.nome END AS clinica,
    o.parametro,
    AVG(o.valor) AS media_valor,
    STDDEV(o.valor) AS desvio_padrao_valor
FROM
    observacao o
JOIN
    consulta co ON o.id = co.id
JOIN
    medico m ON co.nif = m.nif
JOIN
    clinica cl ON co.nome = cl.nome
WHERE
    o.valor IS NOT NULL
GROUP BY
    GROUPING SETS (
        (m.especialidade, m.nome, cl.nome, o.parametro),
        (m.especialidade, m.nome, o.parametro),
        (m.especialidade, o.parametro),
        (o.parametro),
        ()
    )
ORDER BY
    especialidade, medico, clinica, o.parametro;