from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo

# --- ATIVIDADE 1: FUNÇÃO LGPD (ANONIMIZAÇÃO) ---
def LGPD(row):
    nome = row[1].split(" ")

    # Anonimiza o nome, troca as letras por *, exceto a primeira letra
    primeiro = nome[0]
    nome_anon = primeiro[0] + "*" * (len(primeiro) - 1)

    # mantém último sobrenome
    if len(nome) > 1:
        nome_anon += " " + nome[-1]

    # Anonimiza o CPF, substituindo os últimos caracteres por *
    cpf = row[2][:3] + ".***.***-**"

    # Anonimizaa o e-mail, substituindo os caracteres por *
    email_usuario, email_dom = row[3].split("@")
    email = email_usuario[0] + "*" * (len(email_usuario) - 1) + "@" + email_dom

    # Anonimiza o telefone, apresentando somente o final
    telefone = row[4][-4:]

    return (row[0], nome_anon, cpf, email, telefone, row[5], row[6], row[7])

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)
