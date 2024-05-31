import random
import datetime

# Pelo menos 80-100 primeiros e últimos nomes
primeiros_nomes = ['Gabriela', 'Rui', 'David', 'Samuel', 'Camila', 'Ana', 'Gabriela', 'Letícia', 'Carminho', 'Débora', 'Benjamim', 'Íris', 'Catarina', 'Luís', 'Leonor', 'Salomé', 'Afonso', 'Carlota', 'Kelly', 'Rita', 'Hugo', 'Guilherme', 'Pilar', 'Lucas', 'Emília', 'Laura', 'Vitória', 'Wilson', 'Benedita', 'Marcos', 'Marco', 'Jorge', 'Ângela', 'Rúben', 'Mateus', 'Filipe', 'Lourenço', 'William', 'Martim', 'Sofia', 'Isaac', 'Tiago', 'Sara', 'Rafaela', 'Sebastião', 'Henrique', 'Dinis', 'Ismael', 'Mara', 'Vítor', 'Hugo', 'Matilde', 'Nicole', 'Madalena', 'Matias', 'Caetana', 'Camila', 'Henrique', 'Frederico', 'Carminho', 'Naiara', 'Afonso', 'Gustavo', 'Matilde', 'Beatriz', 'Márcio', 'Clara', 'Nuno', 'Rafaela', 'Matias', 'Ariana', 'Vera', 'Rodrigo', 'Pedro', 'Nicole', 'Isaac', 'Clara', 'Larissa', 'Emanuel', 'Eva', 'Maria', 'Ismael', 'Diana', 'Vicente', 'Larissa', 'Álvaro', 'Anita', 'Madalena', 'Violeta', 'Luana']
ultimos_nomes = ['Barros', 'Valente', 'Azevedo', 'Campos', 'Barros', 'Nascimento', 'Marques', 'Assunção', 'Carneiro', 'Martins', 'Moura', 'Monteiro', 'Sá', 'Miranda', 'Loureiro', 'Moreira', 'Ribeiro', 'Carneiro', 'Matos', 'Nogueira', 'Nascimento', 'Silva', 'Silva', 'Tavares', 'Mendes', 'Carvalho', 'Melo', 'Baptista', 'Anjos', 'Mendes', 'Machado', 'Pacheco', 'Rodrigues', 'Carneiro', 'Melo', 'Fonseca', 'Moura', 'Moura', 'Antunes', 'Barros', 'Campos', 'Moura', 'Guerreiro', 'Antunes', 'Magalhães', 'Matias', 'Alves', 'Henriques', 'Ribeiro', 'Lopes', 'Santos', 'Nogueira', 'Baptista', 'Correia', 'Matos', 'Gaspar', 'Leal', 'Pinho', 'Machado', 'Cunha', 'Vaz', 'Ribeiro', 'Barbosa', 'Martins', 'Marques', 'Ramos', 'Paiva', 'Silva', 'Maia', 'Almeida', 'Sá', 'Esteves', 'Pinto', 'Gaspar', 'Vicente', 'Reis', 'Azevedo', 'Borges', 'Pacheco', 'Freitas', 'Pinheiro', 'Marques', 'Figueiredo', 'Miranda', 'Simões', 'Baptista']

# Combinar todos os primeiros e últimos nomes
nomes = [f"{primeiro} {ultimo}" for primeiro in primeiros_nomes for ultimo in ultimos_nomes]

nif = 200000000
# Para a começar em 212000000 para não haver conflitos com os telefones das clínicas
telefone = 213000000

# soma tem de ser 20 + 40
especialidades = [
  # 20 Here
  {"nome": "Clínica geral", "num_medicos": 20},
  # 40 Here
  {"nome": "cardiologia", "num_medicos": 10},
  {"nome": "ortopedia", "num_medicos": 9},
  {"nome": "pediatria", "num_medicos": 8},
  {"nome": "dermatologia", "num_medicos": 7},
  {"nome": "oftalmologia", "num_medicos": 6},
]

# 50 Sintomas quantitativos
sintomas_qualitativos = [
  "Dor de cabeça",
  "Tontura",
  "Náusea",
  "Fadiga",
  "Insônia",
  "Tosse",
  "Falta de ar",
  "Dor no peito",
  "Dor abdominal",
  "Dor de garganta",
  "Coriza",
  "Dores musculares",
  "Dor nas articulações",
  "Dor nas costas",
  "Dor de ouvido",
  "Vermelhidão nos olhos",
  "Visão embaçada",
  "Perda de audição",
  "Erupção cutânea",
  "Coceira",
  "Inchaço",
  "Febre",
  "Calafrios",
  "Suores noturnos",
  "Perda de peso",
  "Ganho de peso",
  "Perda de apetite",
  "Aumento do apetite",
  "Ansiedade",
  "Depressão",
  "Dificuldade para engolir",
  "Palpitações",
  "Dor de dente",
  "Cãibras",
  "Formigamento",
  "Rigidez",
  "Dificuldade para respirar",
  "Sensação de desmaio",
  "Azia",
  "Flatulência",
  "Prurido",
  "Olhos secos",
  "Irritabilidade",
  "Dor ao urinar",
  "Sede excessiva",
  "Fadiga crônica",
  "Dificuldade de concentração",
  "Confusão mental",
  "Dormência",
  "Sangramento nasal"
]
# 20 sintomas quantitativos
observacoes_metricas = [
  {'sintoma': 'índice de massa corporal', 'avg': 67.72, 'std_dev': 1.56},
  {'sintoma': 'nível de potássio', 'avg': 80.64, 'std_dev': 3.94},
  {'sintoma': 'circunferência abdominal', 'avg': 60.71, 'std_dev': 3.09},
  {'sintoma': 'saturação de oxigênio', 'avg': 82.57, 'std_dev': 5.88},
  {'sintoma': 'nível de sódio', 'avg': 59.34, 'std_dev': 7.94},
  {'sintoma': 'nível de oxigênio no sangue', 'avg': 85.83, 'std_dev': 7.44},
  {'sintoma': 'nível de triglicéridos', 'avg': 57.37, 'std_dev': 7.2},
  {'sintoma': 'altura', 'avg': 71.94, 'std_dev': 7.05},
  {'sintoma': 'peso', 'avg': 56.39, 'std_dev': 3.75},
  {'sintoma': 'nível de hemoglobina', 'avg': 67.79, 'std_dev': 7.07},
  {'sintoma': 'nível de glicose', 'avg': 78.7, 'std_dev': 7.28},
  {'sintoma': 'frequência respiratória', 'avg': 90.39, 'std_dev': 4.71},
  {'sintoma': 'frequência cardíaca', 'avg': 76.08, 'std_dev': 7.7},
  {'sintoma': 'taxa de filtração glomerular', 'avg': 78.24, 'std_dev': 7.16},
  {'sintoma': 'capacidade pulmonar', 'avg': 80.75, 'std_dev': 5.52},
  {'sintoma': 'nível de cálcio', 'avg': 73.04, 'std_dev': 8.93},
  {'sintoma': 'nível de creatinina', 'avg': 52.55, 'std_dev': 3.32},
  {'sintoma': 'temperatura corporal', 'avg': 86.36, 'std_dev': 2.84},
  {'sintoma': 'pressão arterial', 'avg': 92.41, 'std_dev': 5.74},
  {'sintoma': 'colesterol', 'avg': 50.06, 'std_dev': 2.05}
]

# Lista com vários medicamentos
# Pelo menos 6 a 10
medicamentos = ["Paracetamol", "Ibuprofeno", "Amoxicilina", "Omeprazol", "Loratadina", "Metaformina", "Benuron", "Ramipril"]


cardiologistas_nifs = []
receitas_paciente0 = []

def dict_to_sql(table_name, data):
  """Converts a list of dictionaries of the same type 
  to a list of SQL INSERT statements."""
  statement = [
    f"-- {len(data)} rows for table {table_name}",
    f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES"
  ]
  for row in data:
    values = ', '.join([f"'{value}'" if value != 'NULL' else 'NULL' for value in row.values()])
    statement.append(f"({values}),")
  statement[-1] = statement[-1][:-1] + ';'
  return '\n' + '\n'.join(statement)

def write_to_file(filename, sql_statements):
  with open(filename, 'w') as f:
    for line in sql_statements:
      f.write(line + '\n')
      # print(line)

def get_morada():
  return f"Rua {random.randint(1,300)}, {random.randint(1000, 2799)}-{random.randint(100, 999)} {random.choice(['Cascais', 'Almada', 'Loures', 'Sintra', 'Montijo'])}"

def date_range(start: datetime.date, stop: datetime.date):
  current = start
  while current <= stop:
    yield current
    current += datetime.timedelta(days=1)

def time_range(start: datetime.time, stop: datetime.time):
  start = datetime.datetime.combine(datetime.datetime.today(), start)
  stop = datetime.datetime.combine(datetime.datetime.today(), stop)
  current = start

  while current <= stop:
    yield current.time()
    if current.time() == datetime.time(12, 30):
      current += datetime.timedelta(minutes=90) # Skips lunch break
    else:
      current += datetime.timedelta(minutes=30)

def gen_next_nif(current_nif: int):
  current_nif += random.randint(69, 6960)

  # NIF control digit
  nif_str = str(current_nif)
  soma = sum([int(digito) * (9 - pos) for pos, digito in enumerate(nif_str)])
  resto = soma % 11
  if resto <= 1:
    control = 0
  else:
    control = 11 - resto

  new_nif = int(nif_str)
  return (new_nif // 10) * 10 + control

def generate_clinicas():
  return [
    {"nome": "Centro de Saude Harmony", "telefone": "273849203", "morada": "Rua Garrett 187, 1500-432 Lisboa"},
    {"nome": "Centro Medico Total Saude", "telefone": "290384750", "morada": "Rua dos Bacalhoeiros 54, 2780-219 Oeiras"},
    {"nome": "Clinica Medica Compassion", "telefone": "265983471", "morada": "Rua de São Bento 98, 2700-578 Amadora"},
    {"nome": "Clinica Alberto Jussuares", "telefone": "237492065", "morada": "Rua do Alecrim 135, 1200-301 Cascais"},
    {"nome": "Clinica Montereal", "telefone": "219384756", "morada": "Rua da Prata, 74, 2670-450 Loures"}
]

def generate_enfermeiros(clinicas):
  enfermeiros = []
  global nif
  global telefone
  for clinica in clinicas:
    for i in range(random.randint(5, 6)):
      enfermeiros.append({
        'nif': str(nif),
        'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
        'telefone': str(telefone),
        'morada': get_morada(),
        'nome_clinica': clinica['nome']
      })
      nif = gen_next_nif(nif)
      telefone += random.randint(6, 696)
  return enfermeiros

def generate_medicos(especialidades):
  medicos = []
  global nif
  global telefone
  for esp in especialidades:
    for _ in range(esp['num_medicos']):
      if esp['nome'] == 'Cardiologia': cardiologistas_nifs.append(str(nif))
      medicos.append({
        'nif': str(nif),
        'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
        'telefone': str(telefone),
        'morada': get_morada(),
        'especialidade': esp['nome']
      })
      nif = gen_next_nif(nif)
      telefone += random.randint(6, 696)
  return medicos

def generate_trabalha(medicos, clinicas):
  while True:
    valid = True
    trabalha = []
    for medico in medicos:
      clinicas_medico_sample = random.sample(clinicas, random.randint(2,4))
      clinicas_medico = [random.choice(clinicas_medico_sample)['nome'] for _ in range(7)]
      while len(set(clinicas_medico)) < 2:
        clinicas_medico = [random.choice(clinicas_medico_sample)['nome'] for _ in range(7)]
      for i in range(7):
        trabalha.append({
          'nif': medico['nif'],
          'nome': clinicas_medico[i],
          'dia_da_semana': i+1
        })
    # Verificar que todas as clinicas têm pelo menos 8 médicos a trabalhar nesse dia da semana
    for clinica in clinicas:
      for dia in range(1, 8):
        if len([t for t in trabalha if t['nome'] == clinica['nome'] and t['dia_da_semana'] == dia]) < 8:
          valid = False
          break
        if not valid: 
          break
    if valid:
      break
  return trabalha

def generate_pacientes(num_pacientes):
  pacientes = []
  global nif
  global telefone
  ssn = 10000000000
  for paciente_id in range(1, num_pacientes + 1):
    data_nasc = datetime.date(random.randint(1950, 2006), random.randint(1, 12), random.randint(1, 28)).isoformat()
    pacientes.append({
      'ssn': str(ssn),
      'nif': str(nif),
      'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
      'telefone': str(telefone),
      'morada': get_morada(),
      'data_nasc': data_nasc
    })
    nif = gen_next_nif(nif)
    telefone += random.randint(6, 696)
    ssn += random.randint(69, 696969)
  return pacientes

def generate_consultas(pacientes, trabalha, clinicas):
  consultas = []
  global nif
  global telefone
  consulta_id = 1
  codigo_sns = 00000000000
  start_date = datetime.date(2023, 1, 1)
  end_date = datetime.date(2024, 5, 31)
  current_date = start_date
  while current_date <= end_date:
    pacientes_hoje = pacientes.copy()
    cooldown = False
    for clinica in clinicas:
      dia_da_semana = current_date.weekday() + 1
      medicos_clinica = [t['nif'] for t in trabalha if t['nome'] == clinica['nome'] and t['dia_da_semana'] == dia_da_semana]
      horas = [f'{str(i).zfill(2)}:{j}:00' for i in range(8, 13) for j in ("00", "30")]
      horas += [f'{str(i).zfill(2)}:{j}:00' for i in range(14, 19) for j in ("00", "30")]
      for medico_nif in medicos_clinica:
        # 3 consultas por médico garante que há pelo menos 
        # 21 consultas por dia nesta clínica
        # Add appointment for cronic pacient (pacient[0]) (tem que ser consulta de cardiologia)
        m = 0
        for hora in random.sample(horas, random.randint(3, 12)):
          if medico_nif in cardiologistas_nifs and not cooldown:
            consultas.append({
              'id': consulta_id,
              'ssn': pacientes_hoje.pop(0)['ssn'],
              'nif': medico_nif,
              'nome': clinica['nome'],
              'data': current_date.isoformat(),
              'hora': hora,
              'codigo_sns': str(codigo_sns).zfill(12)
            })
            receitas_paciente0.append(str(codigo_sns).zfill(12))
            cooldown = True
            m += 1
          else:
            consultas.append({
              'id': consulta_id,
              'ssn': pacientes_hoje.pop(random.randint(m, len(pacientes_hoje) - 1))['ssn'],
              'nif': medico_nif,
              'nome': clinica['nome'],
              'data': current_date.isoformat(),
              'hora': hora,
              'codigo_sns': str(codigo_sns).zfill(12)
            })
          consulta_id += 1
          codigo_sns += random.randint(1, 6968)
    current_date += datetime.timedelta(days=1)
    cooldown = False
  return consultas


def generate_receitas(consultas):
  receitas = []
  for consulta in consultas:
    if random.random() < 0.8:
      if consulta['codigo_sns'] in receitas_paciente0:
        receitas.append({
          'codigo_sns': consulta['codigo_sns'],
          'medicamento': 'Ibuprofeno',
          'quantidade': random.randint(1, 3)
        })
        continue

      for medicamento in random.sample(medicamentos, random.randint(1, 6)):
        receitas.append({
          'codigo_sns': consulta['codigo_sns'],
          'medicamento': medicamento,
          'quantidade': random.randint(1, 3)
        })
    else: 
      consulta['codigo_sns'] = 'NULL'
  return receitas

def generate_observacoes(consultas):
  observacoes = []
  for consulta in consultas:
    # 1 a 5 sintomas qualitativos
    for sintoma in random.sample(sintomas_qualitativos, random.randint(1, 5)):
      observacoes.append({
        'id': consulta['id'],
        'parametro': sintoma,
        'valor': 'NULL'
      })
    # 0 a 3 sintomas quantitativos
    for sintoma in random.sample(observacoes_metricas, random.randint(0, 3)):
      valor = random.normalvariate(sintoma['avg'], sintoma['std_dev'])
      observacoes.append({
        'id': consulta['id'],
        'parametro': sintoma['sintoma'],
        'valor': f'{valor:.2f}'
      })
  return observacoes

def main():
  sql_statements = [
    "-- Eliminar dados anteriores",
    "TRUNCATE TABLE receita, observacao, consulta, trabalha, paciente, medico, enfermeiro, clinica, RESTART IDENTITY;"
  ]
  clinicas = generate_clinicas()
  medicos = generate_medicos(especialidades)
  enfermeiros = generate_enfermeiros(clinicas)
  trabalha = generate_trabalha(medicos, clinicas)
  pacientes = generate_pacientes(5020)
  consultas = generate_consultas(pacientes, trabalha, clinicas)
  receitas = generate_receitas(consultas)
  observacoes = generate_observacoes(consultas)

  sql_statements.append(dict_to_sql('clinica', clinicas))
  sql_statements.append(dict_to_sql('enfermeiro', enfermeiros))
  sql_statements.append(dict_to_sql('medico', medicos))
  sql_statements.append(dict_to_sql('trabalha', trabalha))
  sql_statements.append(dict_to_sql('paciente', pacientes))
  [c.pop('id') for c in consultas] # Removes manual IDs for appointments because they fuck up the serial sequence
  sql_statements.append(dict_to_sql('consulta', consultas))
  sql_statements.append(dict_to_sql('receita', receitas))
  sql_statements.append(dict_to_sql('observacao', observacoes))

  write_to_file('./populate1.sql', sql_statements)

if __name__ == '__main__':
  main()
