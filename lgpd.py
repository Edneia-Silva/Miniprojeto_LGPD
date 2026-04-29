from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Date, DateTime
from decorator_tempo import medir_tempo
from datetime import datetime
import csv
import os

os.makedirs("anos", exist_ok=True)

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2")

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

# --- ATIVIDADE 1: ANONIMIZAÇÃO ---
# Anonimiza o nome, troca as letras por *, exceto a primeira letra, mantém sobrenome (Ex.: O***** Araújo)
def LGPD(row):
    nome = row[1].split(" ")  
    nome_anon = nome[0][0] + "*" * (len(nome[0]) - 1)
    
    if len(nome) > 1:
        nome_anon += " " + nome[-1]

    # Anonimiza o CPF, mantém os 3 primeiros números e substitui o restante por * (Ex.: 237.***.***-**)
    cpf = row[2][:3] + ".***.***-**"

    # Anonimiza o e-mail, substituindo os caracteres por * (Ex.: n*********@example.com)
    email_usuario, email_dom = row[3].split("@")
    email = email_usuario[0] + "*" * (len(email_usuario) - 1) + "@" + email_dom

    # Anonimiza o telefone: apresenta somente os 4 números finais (Ex.: 6810)
    telefone = row[4][-4:]

    return (row[0], nome_anon, cpf, email, telefone, row[5])


# --- BUSCA DADOS UMA VEZ SÓ ---
def buscar_usuarios():
    with engine.connect() as conn:
        return list(conn.execute(text("SELECT * FROM usuarios;")))

print("\n--- ATIVIDADE 1: AMOSTRA LGPD (ANONIMIZAÇÃO) ---")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))

    for row in result:
        print(LGPD(row))

print("---------------------------------\n")


# --- ATIVIDADE 2: CRIA ARQUIVOS POR ANO ---
# Gerar arquivos por ano (anonimizados)
@medir_tempo
def atividade2():
    usuarios = buscar_usuarios()
    dados_por_ano = {}

    for row in usuarios:
        user = LGPD(row)
        ano = user[5].year

        if ano not in dados_por_ano:
            dados_por_ano[ano] = []

        dados_por_ano[ano].append(user)

    for ano, lista in dados_por_ano.items():
        with open(f"anos/{ano}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nome", "cpf", "email", "telefone", "data_nascimento"])

            for u in lista:
                writer.writerow(u)

print("Atividade 2 concluída - arquivos por ano gerados")


# --- ATIVIDADE 3 ---
# Gerar todos.csv sem anonimização
@medir_tempo
def atividade3():
    usuarios = buscar_usuarios()

    with open("todos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "cpf"])
        
        for u in usuarios:
            writer.writerow([u[1], u[2]])

print("Atividade 3 concluída - arquivo todos.csv gerado")


# --- ATIVIDADE 4 ---
# Medir tempo + salvar em log usando decorator
# Não tem função nova. Esse decorator foi aplicado nas funções 
# das atividades 2 e 3; registrando os tempos em arquivo de log.

# --- EXECUÇÃO ---
atividade2()
atividade3()