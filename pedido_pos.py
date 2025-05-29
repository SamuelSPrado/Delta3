from DataBase.database import get_connection

def consulta_transacao_offline(local, caixa):
    query = """
    SELECT 
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 1 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'CRÉDITO [NT]',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 2 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DÉBITO [NT]',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 3 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DINHEIRO',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO NOT IN (1, 2, 3) THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'OUTROS',
        FORMAT(SUM(PP.DESCONTO), 'N', 'PT-BR') AS 'DESCONTO',
        FORMAT(SUM(T.VALOR), 'N', 'PT-BR') AS 'TOTAL TRANSAÇÃO OFFLINE'
    FROM VWTRANSACAOOFFLINE T
    JOIN VWPEDIDOPOS PP ON T.PEDIDOPOSID = PP.ID
    WHERE T.LOCALCLIENTEID = ? AND PP.SESSAOPOSID = ? AND T.STATUS NOT IN (5);
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (local, caixa))
        return cursor.fetchone()

def consulta_transacao_pos(local, caixa):
    query = """
    SELECT 
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 1 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [CRÉDITO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 2 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [DÉBITO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 3 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [DINHEIRO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO NOT IN (1, 2, 3) THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [OUTROS],
        FORMAT(SUM(PP.DESCONTO), 'N', 'PT-BR') AS [DESCONTO],
        FORMAT(SUM(T.VALOR), 'N', 'PT-BR') AS 'TOTAL TRANSAÇÃO ONLINE'
    FROM VWTRANSACAOPOS T
    JOIN VWPEDIDOPOS PP ON T.PEDIDOPOSID = PP.ID
    WHERE T.LOCALCLIENTEID = ? AND PP.SESSAOPOSID = ? AND T.STATUS NOT IN (5);
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (local, caixa))
        return cursor.fetchone()
