-- (RI-1)
CREATE OR REPLACE FUNCTION check_consulta_schedule()
RETURNS TRIGGER AS
$$
BEGIN
    -- Verificar primeiro se a hora está correta (hora cheia ou meia hora)
    IF EXTRACT(MINUTE FROM NEW.hora) NOT IN (0, 30) THEN
        RAISE EXCEPTION 'As consultas devem ser marcadas à hora cheia ou meia-hora dentro dos intervalos de 8h-13h e 14h-19h.';
    END IF;

    -- Em seguida, verificar as restrições de horas válidas, incluindo restrição para 13:30 e 19:30
    IF NOT ((EXTRACT(HOUR FROM NEW.hora) BETWEEN 8 AND 12 OR EXTRACT(HOUR FROM NEW.hora) BETWEEN 14 AND 18) OR
            (EXTRACT(HOUR FROM NEW.hora) = 13 AND EXTRACT(MINUTE FROM NEW.hora) = 0) OR
            (EXTRACT(HOUR FROM NEW.hora) = 19 AND EXTRACT(MINUTE FROM NEW.hora) = 0)) THEN
        RAISE EXCEPTION 'A hora da consulta (%s) está fora do horário permitido de funcionamento ou é um horário não aceite (13:30 ou 19:30).', NEW.hora::time;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Recriar o trigger com a função atualizada
DROP TRIGGER IF EXISTS consulta_schedule_trigger ON consulta;

CREATE TRIGGER consulta_schedule_trigger
BEFORE INSERT OR UPDATE ON consulta
FOR EACH ROW EXECUTE FUNCTION check_consulta_schedule();

-- (RI-2)
CREATE OR REPLACE FUNCTION check_medico_self_consult()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o médico é o mesmo que o paciente
    IF EXISTS (SELECT 1 FROM paciente WHERE ssn = NEW.ssn AND nif = NEW.nif) THEN
        RAISE EXCEPTION 'Um médico não pode se consultar a si próprio.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS medico_self_consult_trigger ON consulta;

CREATE TRIGGER medico_self_consult_trigger
BEFORE INSERT OR UPDATE ON consulta
FOR EACH ROW EXECUTE FUNCTION check_medico_self_consult();

-- (RI-3)
CREATE OR REPLACE FUNCTION check_medico_clinica_dia() RETURNS TRIGGER AS $$
DECLARE
    dia_semana INTEGER;
BEGIN
    -- Extrair o dia da semana da data da consulta (1=Domingo, 7=Sábado)
    dia_semana := EXTRACT(DOW FROM NEW.data);
    -- Ajustar dia da semana para (1=Segunda, 7=Domingo)
    IF dia_semana = 0 THEN
        dia_semana := 7;
    END IF;

    -- Verificar se o médico está escalado para trabalhar na clínica nesse dia da semana
    IF NOT EXISTS (
        SELECT 1
        FROM trabalha
        WHERE trabalha.nif = NEW.nif
        AND trabalha.nome = NEW.nome
        AND trabalha.dia_da_semana = dia_semana
    ) THEN
        RAISE EXCEPTION 'O médico % não está escalado para trabalhar na clínica % no dia %.', NEW.nif, NEW.nome, TO_CHAR(NEW.data, 'Day');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_medico_clinica_dia
BEFORE INSERT OR UPDATE ON consulta
FOR EACH ROW
EXECUTE FUNCTION check_medico_clinica_dia();