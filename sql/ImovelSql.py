SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS imovel (
    id           INTEGER         PRIMARY KEY AUTOINCREMENT,
    nome         TEXT            NOT NULL,
    preco        INTEGER         NOT NULL,
    descricao    TEXT            NOT NULL,
    categoria    TEXT            NOT NULL,
    destaque     INETEGER        NOT NULL
    )
"""

SQL_INSERIR_IMOVEL = """
    INSERT INTO imovel (nome, preco, descricao, categoria, destaque)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE imovel
    SET nome=?, preco=?, descricao=?, categoria=?, destaque=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM imovel
    WHERE id=?
"""

SQL_PESQUISAR = """
    SELECT id, nome, preco, descricao, categoria
    FROM imovel
    WHERE categoria = ? AND nome = LIKE "%?%"
    ORDER BY nome    
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, preco, descricao, categoria
    FROM imovel
    ORDER BY nome
"""

SQL_OBTER_DESTAQUES = """
    SELECT id, nome, preco, descricao, categoria, destaque
    FROM imovel
    WHERE destaque = ?
    ORDER BY nome
"""

SQL_OBTER_CATEGORIA = """
    SELECT id, nome, preco, descricao, categoria
    FROM imovel
    WHERE categoria = ?
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, preco, descricao, categoria
    FROM imovel
    WHERE id=?
"""