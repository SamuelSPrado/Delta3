def agrupar_pagamentos(orders):
    tipos = {'CREDITO': 0, 'DEBITO': 0, 'DINHEIRO': 0, 'OUTROS': 0}
    for order in orders:
        if order['Status'] == 'PAGAMENTO REALIZADO':
            for payment in order['Payments']:
                tipo = payment['Type']
                valor = payment['Value']
                if tipo == 'CREDITO':
                    tipos['CREDITO'] += valor
                elif tipo == 'DEBITO':
                    tipos['DEBITO'] += valor
                elif tipo == 'DINHEIRO':
                    tipos['DINHEIRO'] += valor
                else:
                    tipos['OUTROS'] += valor
    return tipos