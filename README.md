## 📚 Sistema de Tratamento de Dados - Miniprojeto_LGPD
========  Projeto Fatec Rio Claro - LGPD  =========

Este projeto tem como objetivo aplicar os conceitos da **LGPD (Lei Geral de Proteção de Dados)** em um sistema de banco de dados, realizando a anonimização de dados sensíveis e gerando relatórios de exportação

## 🚀 Funcionalidades

- Atividade 1 (Anonimização): tratamento de dados sensíveis (Nome, CPF, E-mail e Telefone) utilizando técnicas de mascaramento.
- Atividade 2 (Organização por ano): exportação de dados anonimizados em arquivos CSV separados por ano de nascimento, organizados na pasta `/anos`.
- Atividade 3 (Relatório geral): geração de um arquivo `todos.csv` contendo apenas Nome e CPF originais (sem anonimização).
- Atividade 4 (Monitoramento): implementação de um **Decorator** personalizado para medir o tempo de execução das tarefas e registrar em um arquivo `log.txt`.

## 🛠️ Tecnologias e Bilbiotecas

- Python 3.12: linguagem base para toda a lógica de anonimização e processamento
- SQLAlchemy: utilizado como ORM/Toolkit para gerenciar a conexão com o banco de dados e o mapeamento da tabela usuarios.
- Psycopg2-binary: driver essencial para a comunicação entre o Python e o servidor PostgreSQL.

== Biblioteca Padrão (Builts-ins) ==:
- CSV: para a geração precisa dos relatórios .csv por ano e consolidados. 
- Functools (wraps): aplicado no decorador para preservar os metadados das funções monitoradas.
- Os & datetime: para manipulação de diretórios e tratamento de datas de nascimento.

## 📁 Estrutura de Arquivos

- `/anos`: contém os arquivos CSV segmentados por ano.
- `lgpd.py`: script principal contendo a lógica de negócio e exportação.
- `decorator_tempo.py`: módulo do decorador de medição de tempo para o monitoramento de performance.
- `.gitignore`: configurado para não versionar dados sensíveis (CSVs) e logs locais.
- `requirements.txt`: lista de dependências externas para execução do projeto.
- `log.txt`: registro automático de tempo das execuções realizadas.

## 🚀 Como executar

1. Certifique-se de estar com seu ambiente virtual (.venv) ativo.

2. Instale as dependências necessárias:
   - pip install -r requirements.txt

3. Execute o script principal:
   - python lgpd.py

4. Os resultados serão gerados na pasta /anos e na raiz do projeto como todos.csv.


