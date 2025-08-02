import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "agendas.db")

def banco_agendamento():
    print("estamos iniciando a configuração do banco de dados...")

    try:
        with sqlite3.connect(DB_PATH) as conexao:
            cursor = conexao.cursor()
            comando_sql = """
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY,
                    local TEXT,
                    data_hora TEXT,
                    descricao TEXT
                ); """
            cursor.execute(comando_sql)
            print("banco de dados pronto para uso")
    except sqlite3.Error as e:
        print(f"erro no banco de dados: {e}")


def registrar(reg_local:str, reg_horario:str, reg_descricao:str):
    dados = (reg_local, reg_horario, reg_descricao)
    insert = ("INSERT INTO agendamentos(local, data_hora, descricao) VALUES (?,?,?)")

    try:
        with sqlite3.connect(DB_PATH) as conexao:
            cursor = conexao.cursor()
            cursor.execute(insert, dados)
            print("registro bem sucedido")
    except sqlite3.Error as e:
        print(f"erro ao registrar: {e}")

    print("Configuração do banco de dados concluída.")


def historico():
    print("buscando historico da consulta...")

    try:
        with sqlite3.connect(DB_PATH) as conexao:
            print(f"Conectado ao banco: {DB_PATH}")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, local, data_hora, descricao FROM agendamentos ORDER BY id DESC")
            registro = cursor.fetchall()
            print(f"Registros encontrados: {registro}")
            return registro
    except sqlite3.Error as e:
        print(f"Erro na consulta: {e}")
        return []
    
def deletar(delet_id):
    print(f"tentando apagar agendamento com o id: {delet_id}")

    try:
        with sqlite3.connect(DB_PATH) as conexao:
            cursor = conexao.cursor()
            comando_delete = "DELETE FROM agendamentos WHERE id = ?"
            cursor.execute(comando_delete, (delet_id,))
            if cursor.rowcount > 0:
                print(f"sucesso ao deletar o id: {delet_id}")
            else:
                print(f"nao encontramos o id: {delet_id}")
    except sqlite3.Error as e:
        print(f"erro {e}")

banco_agendamento()