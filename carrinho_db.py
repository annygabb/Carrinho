"""
Módulo de persistência do Carrinho de Compras — UniPay/ShopFast
Utiliza SQLite como banco de dados relacional embutido no Python.

Aula 11 — Teste de Software (2026.1) | UniCode UniEvangelica
Professor: Esp. Carlos Roberto Gomes Júnior
"""

import sqlite3
from typing import List, Dict

def criar_tabela(conn: sqlite3.Connection) -> None:
    """
    Cria a tabela 'carrinho' no banco recebido, se ainda não existir.
    Esquema: id (PK), nome (TEXT), preco (REAL), quantidade (INTEGER).
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrinho (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT    NOT NULL,
            preco      REAL    NOT NULL CHECK(preco >= 0),
            quantidade INTEGER NOT NULL DEFAULT 1 CHECK(quantidade > 0)
        )
    """)
    conn.commit()

def adicionar_item(
    conn: sqlite3.Connection, 
    nome: str, 
    preco: float, 
    quantidade: int = 1
) -> int:
    """
    Insere um item no carrinho e retorna o id gerado.
    Raises:
        ValueError: se preco < 0 ou quantidade <= 0.
    """
    if preco < 0:
        raise ValueError(f"Preço não pode ser negativo: {preco}")
    if quantidade <= 0:
        raise ValueError(f"Quantidade deve ser maior que zero: {quantidade}")

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO carrinho (nome, preco, quantidade) VALUES (?, ?, ?)",
        (nome, preco, quantidade)
    )
    conn.commit()
    return cursor.lastrowid

def listar_itens(conn: sqlite3.Connection) -> List[Dict]:
    """
    Retorna todos os itens do carrinho como uma lista de dicionários.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco, quantidade FROM carrinho")
    rows = cursor.fetchall()
    return [
        {"id": row[0], "nome": row[1], "preco": row[2], "quantidade": row[3]}
        for row in rows
    ]

def calcular_total(conn: sqlite3.Connection) -> float:
    """
    Calcula o valor total do carrinho (preco * quantidade).
    Retorna 0.0 se o carrinho estiver vazio.
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(preco * quantidade), 0.0) FROM carrinho"
    )
    resultado = cursor.fetchone()[0]
    return float(resultado)

def limpar_carrinho(conn: sqlite3.Connection) -> int:
    """
    Remove todos os itens da tabela carrinho.
    Returns: Número de linhas removidas.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrinho")
    conn.commit()
    return cursor.rowcount

if __name__ == "__main__":
    conn = sqlite3.connect("carrinho_demo.db")
    criar_tabela(conn)
    
    print("=== Demo Interativa — Carrinho SQLite ===\n")

    adicionar_item(conn, "Notebook Dell", 4500.00, 1)
    adicionar_item(conn, "Mouse Logitech", 150.00, 2)
    adicionar_item(conn, "Teclado Mecânico", 350.00, 1)

    print("Itens no carrinho:")
    for item in listar_itens(conn):
        subtotal = item["preco"] * item["quantidade"]
        print(f"  [{item['id']}] {item['nome']:20s} "
              f"R$ {item['preco']:8.2f} x {item['quantidade']} = R$ {subtotal:.2f}")

    print(f"\nTotal Geral: R$ {calcular_total(conn):.2f}")

    limpar_carrinho(conn)
    print(f"\nCarrinho limpo. Itens restantes: {len(listar_itens(conn))}")
    conn.close()