from DataBase.database import get_connection

def consulta_invoice_order(local, caixa):
    query = """
    SELECT 
        FORMAT(SUM(CASE WHEN FP.CODIGO = 1 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS CREDITO,
        FORMAT(SUM(CASE WHEN FP.CODIGO = 2 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS DEBITO,
        FORMAT(SUM(CASE WHEN FP.CODIGO = 3 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS DINHEIRO,
        FORMAT(SUM(CASE WHEN FP.CODIGO = 100 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS OUTROS,
        FORMAT(SUM(IV.DISCOUNT), 'N', 'PT-BR') AS DESCONTO,
        FORMAT(SUM(OP.VALUE), 'N', 'PT-BR') AS TOTAL_CAIXA_INVOICE
    FROM VWINVOICEORDER IV
    INNER JOIN VWORDERPAYMENT OP ON IV.ID = OP.ORDER_ID
    INNER JOIN VWFORMAPAGAMENTO FP ON OP.FORMOFPAYMENT_ID = FP.ID
    LEFT JOIN VWPEDIDOPOS PP ON IV.ID = PP.ID
    WHERE IV.OWNER_ID = ? AND IV.CASHIER_ID = ? AND PP.STATUS = 3;
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (local, caixa))
        return cursor.fetchone()
