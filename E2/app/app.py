#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig

from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

from decimal import Decimal
from datetime import datetime

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger

@app.route("/", methods=("GET",))
def lista_clinicas():
    """Lista todas as clínicas (nome e morada)."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            clinicas = cur.execute(
                """
                SELECT nome, morada FROM clinica
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(clinicas), 200


@app.route("/c/<clinica>/", methods=("GET",))
def lista_especialidades(clinica):
    """Lista todas as especialidades oferecidas na <clinica>."""
    
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Verifica se <clinica> existe
            clinica_existe = cur.execute(
                "SELECT COUNT(*) FROM clinica WHERE nome = %(clinica)s",
                {"clinica": clinica}
            ).fetchone()[0] > 0

            if not clinica_existe:
                return jsonify({"message": f"{clinica} NOT FOUND", "status": "error"}), 404
            
            especialidades = cur.execute(
                """
                SELECT DISTINCT especialidade
                FROM medico
                WHERE nif IN (SELECT DISTINCT nif FROM trabalha WHERE nome = %(clinica)s)
                """,
                {"clinica": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200
    

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def lista_medicos(clinica, especialidade):
    """Lista todos os médicos (nome) da <especialidade> que trabalham na <clínica>
    e os primeiros três horários disponíveis para consulta de cada um deles (data e hora)."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Verifica se <clinica> existe
            clinica_existe = cur.execute(
                "SELECT COUNT(*) FROM clinica WHERE nome = %(clinica)s",
                {"clinica": clinica}
            ).fetchone()[0] > 0

            if not clinica_existe:
                return jsonify({"message": f"{clinica} NOT FOUND", "status": "error"}), 404

            # Verifica se <especialidade> existe
            especialidade_existe = cur.execute(
                "SELECT COUNT(*) FROM medico WHERE especialidade = %(especialidade)s",
                {"especialidade": especialidade}
            ).fetchone()[0] > 0

            if not especialidade_existe:
                return jsonify({"message": f"{especialidade} NOT FOUND", "status": "error"}), 404
            
            try:
                with conn.transaction():
                    medicos = cur.execute(
                        """
                        SELECT nome
                        FROM medico
                        WHERE nif IN (SELECT nif FROM trabalha WHERE nome = %(clinica)s)
                            AND especialidade = %(especialidade)s
                        """,
                        {"clinica": clinica, "especialidade": especialidade},
                    ).fetchall()

                    if medicos is None:
                        raise Exception(f"A clínica {clinica} não tem médicos da especialidade {especialidade}.")
            
                    result = []
                    for medico in medicos:
                        consultas = cur.execute(
                            """
                            SELECT data, hora
                            FROM horarios_disponiveis
                                JOIN trabalha t ON t.nif = (SELECT nif FROM medico WHERE nome = %(medico)s)
                                    AND t.nome = %(clinica)s
                                    AND t.dia_da_semana = EXTRACT(ISODOW FROM data)
                            WHERE data > CURRENT_DATE OR (data = CURRENT_DATE AND hora > CURRENT_TIME)
                            
                            EXCEPT
                            SELECT data, hora FROM consulta
                            WHERE nif = (SELECT nif FROM medico WHERE nome = %(medico)s)
                            
                            ORDER BY data, hora
                            LIMIT 3
                            """,
                            {"medico": medico[0], "clinica": clinica},
                        ).fetchall()
                        
                        consultas = [[row[0].strftime("%Y-%m-%d"), row[1].strftime("%H:%M")] for row in consultas]
                        result.append([medico, consultas])
                    
                
            except Exception as e:
                    return jsonify({"message": str(e), "status": "error"}), 500
           
            log.debug(f"Found {len(result)} medicos.")
    return jsonify(result), 200

    
@app.route("/a/<clinica>/registar/", methods=("POST",))
def registar_consulta(clinica):
    """Regista uma marcação de consulta na <clinica>.
    Recebe como argumentos um paciente, um médico, 
    e uma data e hora (posteriores ao momento de agendamento)."""
    
    paciente_ssn = request.args.get("paciente_ssn")
    medico_nif = request.args.get("medico_nif")
    data_consulta = request.args.get("data_consulta")
    hora_consulta = request.args.get("hora_consulta")

    # Verificar inputs paciente e medico
    if not (paciente_ssn.isdigit() and len(paciente_ssn) == 11):
        return jsonify({"message": "SSN do paciente inválido.", "status": "error"}), 400
    if not (medico_nif.isdigit() and len(medico_nif) == 9):
        return jsonify({"message": "NIF do médico inválido.", "status": "error"}), 400

    # Verificar inputs data e hora
    try:
        datetime.strptime(data_consulta, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato inválido para data.", "status": "error"}), 400
    try:
        datetime.strptime(hora_consulta, '%H:%M')
    except ValueError:
        return jsonify({"message": "Formato inválido para hora.", "status": "error"}), 400
    
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Verifica se <clinica> existe
            clinica_existe = cur.execute(
                "SELECT COUNT(*) FROM clinica WHERE nome = %(clinica)s",
                {"clinica": clinica}
            ).fetchone()[0] > 0

            if not clinica_existe:
                return jsonify({"message": f"{clinica} NOT FOUND", "status": "error"}), 404
            
            try:
                with conn.transaction():
                    # BEGIN is executed, a transaction started

                    # Verificar se o SSN do paciente existe
                    paciente_existe = cur.execute(
                        """
                        SELECT COUNT(*) FROM paciente WHERE ssn = %(paciente_ssn)s
                        """,
                        {"paciente_ssn": paciente_ssn},
                    ).fetchone()[0] > 0

                    if not paciente_existe:
                        raise Exception("Paciente não encontrado.")

                    # verificar se o NIF do medico existe
                    medico = cur.execute(
                        """
                        SELECT COUNT(*) FROM medico WHERE nif = %(medico_nif)s
                        """,
                        {"medico_nif": medico_nif},
                    ).fetchone()

                    medico_existe = medico[0] > 0

                    if not medico_existe:
                        raise Exception("Médico não encontrado.")

                    # Verificar se a data e hora são posteriores à atual
                    current_datetime = datetime.now()
                    consulta_datetime = datetime.strptime(f"{data_consulta} {hora_consulta}", "%Y-%m-%d %H:%M")

                    if consulta_datetime <= current_datetime:
                        raise Exception("A data e hora da consulta devem ser futuras.")
                    
                    medico = cur.execute(
                        """
                        SELECT COUNT(*)
                        FROM trabalha WHERE nif = %(medico_nif)s
                            AND nome = %(clinica)s
                            AND dia_da_semana = EXTRACT(ISODOW FROM CAST(%(data_consulta)s AS DATE))
                        """,
                        {"medico_nif": medico_nif, "clinica": clinica, "data_consulta": data_consulta},
                    ).fetchone()
                    
                    medico_trabalha_na_clinica_na_data = medico[0] > 0
                    
                    if not medico_trabalha_na_clinica_na_data:
                        raise Exception(f"O médico {medico_nif} não trabalha na clínica {clinica} na data {data_consulta}.")

                    # Verificar se o horário está disponível
                    horario = cur.execute(
                        """
                        SELECT COUNT(*)
                        FROM consulta
                        WHERE nif = %(medico_nif)s
                            AND data = %(data_consulta)s
                            AND hora = %(hora_consulta)s
                        """,
                        {"medico_nif": medico_nif, "data_consulta": data_consulta, "hora_consulta": hora_consulta},
                    ).fetchone()
                    
                    horario_disponivel = horario[0] == 0

                    if not horario_disponivel:
                        raise Exception(f"O horário {data_consulta} {hora_consulta} não está disponível para o médico \
{medico_nif}.")

                    max_id = cur.execute("SELECT MAX(id) FROM consulta").fetchone()[0]
                    next_id = max_id + 1 if max_id else 1
                    
                    cur.execute(
                        """
                        INSERT INTO consulta (id, ssn, nif, nome, data, hora)
                        VALUES (%(next_id)s, %(paciente_ssn)s, %(medico_nif)s, %(clinica)s, %(data_consulta)s, 
                        %(hora_consulta)s)
                        """,
                        {"next_id": next_id, "paciente_ssn": paciente_ssn, "medico_nif": medico_nif,
                        "clinica": clinica, "data_consulta": data_consulta, "hora_consulta": hora_consulta},
                    )
                    
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 500
        
    return jsonify({"message": "Consulta registada com sucesso.", "status": "success"}), 200


@app.route("/a/<clinica>/cancelar/", methods=("DELETE", "POST",))
def cancelar_consulta(clinica):
    """Cancela uma marcação de consulta que ainda não se realizou na <clinica>
    (o seu horário é posterior ao momento do cancelamento).
    Recebe como argumentos um paciente, um médico, e uma data e hora."""
    
    paciente_ssn = request.args.get("paciente_ssn")
    medico_nif = request.args.get("medico_nif")
    data_consulta = request.args.get("data_consulta")
    hora_consulta = request.args.get("hora_consulta")

    # Verificar inputs paciente e medico
    if not (paciente_ssn.isdigit() and len(paciente_ssn) == 11):
        return jsonify({"message": "SSN do paciente inválido.", "status": "error"}), 400
    if not (medico_nif.isdigit() and len(medico_nif) == 9):
        return jsonify({"message": "NIF do médico inválido.", "status": "error"}), 400

    # Verificar inputs data e hora
    try:
        datetime.strptime(data_consulta, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato inválido para data.", "status": "error"}), 400
    try:
        datetime.strptime(hora_consulta, '%H:%M')
    except ValueError:
        return jsonify({"message": "Formato inválido para hora.", "status": "error"}), 400
        
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Verifica se <clinica> existe
            clinica_existe = cur.execute(
                "SELECT COUNT(*) FROM clinica WHERE nome = %(clinica)s",
                {"clinica": clinica}
            ).fetchone()[0] > 0

            if not clinica_existe:
                return jsonify({"message": f"{clinica} NOT FOUND", "status": "error"}), 404

            try:
                with conn.transaction():
                    # BEGIN is executed, a transaction started

                    # Verificar se o SSN do paciente existe
                    paciente_existe = cur.execute(
                        """
                        SELECT COUNT(*) FROM paciente WHERE ssn = %(paciente_ssn)s
                        """,
                        {"paciente_ssn": paciente_ssn},
                    ).fetchone()[0] > 0

                    if not paciente_existe:
                        raise Exception("Paciente não encontrado.")

                    # verificar se o NIF do medico existe
                    medico = cur.execute(
                        """
                        SELECT COUNT(*) FROM medico WHERE nif = %(medico_nif)s
                        """,
                        {"medico_nif": medico_nif},
                    ).fetchone()

                    medico_existe = medico[0] > 0

                    if not medico_existe:
                        raise Exception("Médico não encontrado.")

                    # Verificar se a data e hora são posteriores à atual
                    current_datetime = datetime.now()
                    consulta_datetime = datetime.strptime(f"{data_consulta} {hora_consulta}", "%Y-%m-%d %H:%M")

                    if consulta_datetime <= current_datetime:
                        raise Exception("A data e hora da consulta devem ser futuras.")
                    
                    cur.execute(
                        """
                        DELETE FROM consulta
                        WHERE ssn = %(paciente_ssn)s AND nif = %(medico_nif)s
                          AND nome = %(clinica)s AND data = %(data_consulta)s AND hora = %(hora_consulta)s
                          AND (data > CURRENT_DATE OR (data = CURRENT_DATE AND hora > CURRENT_TIME))
                        """,
                        {"paciente_ssn": paciente_ssn, "medico_nif": medico_nif, "clinica": clinica,
                         "data_consulta": data_consulta, "hora_consulta": hora_consulta},
                    )
                    
                    if cur.rowcount == 0:
                        raise Exception("Consulta não encontrada.")
                                           
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 400
        
        return jsonify({"message": "Consulta cancelada com sucesso.", "status": "success"}), 200



if __name__ == "__main__":
    app.run()
