from sqlalchemy import create_engine, text
import csv
from decorator_tempo import medir_tempo
import os

os.makedirs("anos", exist_ok=True)

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2")


# --- ATIVIDADE 1: ANONIMIZAÇÃO ---
def LGPD(row):
    nome = row[1].split(" ")  # Anonimiza o nome, troca as letras por *, exceto a primeira letra
    nome_anon = nome[0][0] + "*" * (len(nome[0]) - 1)

    # mantém último sobrenome
    if len(nome) > 1:
        nome_anon += " " + nome[-1]

    # Anonimiza o CPF, substituindo os últimos caracteres por *
    cpf = row[2][:3] + ".***.***-**"

    # Anonimiza o e-mail, substituindo os caracteres por *
    email_usuario, email_dom = row[3].split("@")
    email = email_usuario[0] + "*" * (len(email_usuario) - 1) + "@" + email_dom

    # Anonimiza o telefone, apresentando somente o final
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


# --- ATIVIDADE 2:  ---
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
# das atividades 2 e 3, registrando os tempos em arquivo de log.

# --- EXECUÇÃO ---
atividade2()
atividade3()