
import sqlite3
from pathlib import Path

# Local onde o banco será armazenado
CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "aproveitai.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade REAL NOT NULL,
            unidade TEXT NOT NULL,
            validade TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_alimento(nome, quantidade, unidade, validade):
    conexao = conectar()

    conexao.execute("""
        INSERT INTO alimentos (nome, quantidade, unidade, validade)
        VALUES (?, ?, ?, ?)
    """, (nome, quantidade, unidade, validade))

    conexao.commit()
    conexao.close()


def listar_alimentos():
    conexao = conectar()
    conexao.row_factory = sqlite3.Row

    alimentos = conexao.execute("""
        SELECT * FROM alimentos
        ORDER BY validade IS NULL, validade
    """).fetchall()

    conexao.close()

    return alimentos


def excluir_alimento(id_alimento):
    conexao = conectar()

    conexao.execute("""
        DELETE FROM alimentos WHERE id = ?
    """, (id_alimento,))

    conexao.commit()
    conexao.close()


def atualizar_alimento(id_alimento, nome, quantidade, unidade, validade):
    conexao = conectar()

    conexao.execute("""
        UPDATE alimentos
        SET nome = ?, quantidade = ?, unidade = ?, validade = ?
        WHERE id = ?
    """, (nome, quantidade, unidade, validade, id_alimento))

    conexao.commit()
    conexao.close()
