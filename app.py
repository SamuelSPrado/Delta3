import os
import sys

# Adicionar diretório do projeto original ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
import cashier_get
import simple_sales
import invoice_order
import pedido_pos
import utils

app = Flask(__name__)

@app.route('/')
def index():
    """Rota principal que renderiza a página inicial"""
    return render_template('index.html')

@app.route('/api/cashier/<caixa_id>', methods=['GET'])
def get_cashier_info_api(caixa_id):
    """API para obter informações do caixa"""
    try:
        start, end = cashier_get.get_cashier_info(caixa_id)
        return jsonify({
            'success': True,
            'start': start,
            'end': end
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/invoice-order', methods=['POST'])
def analyze_invoice_order():
    """API para analisar Invoice Order"""
    try:
        data = request.json
        local_id = data.get('local_id')
        caixa_id = data.get('caixa_id')
        
        if not local_id or not caixa_id:
            return jsonify({
                'success': False,
                'error': 'LOCAL_ID e CAIXA_ID são obrigatórios'
            }), 400
        
        result = invoice_order.consulta_invoice_order(local_id, caixa_id)
        
        # Converter resultado para dicionário
        if result:
            return jsonify({
                'success': True,
                'data': {
                    'credito': result[0],
                    'debito': result[1],
                    'dinheiro': result[2],
                    'outros': result[3],
                    'desconto': result[4],
                    'total': result[5]
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Nenhum resultado encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/pedido-pos', methods=['POST'])
def analyze_pedido_pos():
    """API para analisar Pedido POS (combinando online e offline)"""
    try:
        data = request.json
        local_id = data.get('local_id')
        caixa_id = data.get('caixa_id')
        
        if not local_id or not caixa_id:
            return jsonify({
                'success': False,
                'error': 'LOCAL_ID e CAIXA_ID são obrigatórios'
            }), 400
        
        # Obter resultados de transações offline e online
        offline_result = pedido_pos.consulta_transacao_offline(local_id, caixa_id)
        online_result = pedido_pos.consulta_transacao_pos(local_id, caixa_id)
        
        # Converter resultados para dicionário
        if offline_result and online_result:
            return jsonify({
                'success': True,
                'data': {
                    'offline': {
                        'credito': offline_result[0],
                        'debito': offline_result[1],
                        'dinheiro': offline_result[2],
                        'outros': offline_result[3],
                        'desconto': offline_result[4],
                        'total': offline_result[5]
                    },
                    'online': {
                        'credito': online_result[0],
                        'debito': online_result[1],
                        'dinheiro': online_result[2],
                        'outros': online_result[3],
                        'desconto': online_result[4],
                        'total': online_result[5]
                    }
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Nenhum resultado encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/simple-sales', methods=['POST'])
def analyze_simple_sales():
    """API para analisar Simple Sales API"""
    try:
        data = request.json
        local_id = data.get('local_id')
        caixa_id = data.get('caixa_id')
        
        if not local_id or not caixa_id:
            return jsonify({
                'success': False,
                'error': 'LOCAL_ID e CAIXA_ID são obrigatórios'
            }), 400
        
        # Obter datas do caixa
        start, end = cashier_get.get_cashier_info(caixa_id)
        
        # Obter dados da API Simple Sales
        sales_data = simple_sales.get_simple_sales(local_id, start, end)
        
        # Agrupar pagamentos
        agrupados = utils.agrupar_pagamentos(sales_data['Orders'])
        
        # Calcular total
        total = sum(agrupados.values())
        
        # Formatar valores para o padrão brasileiro
        formatted_result = {
            'credito': f"{agrupados['CREDITO']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'debito': f"{agrupados['DEBITO']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'dinheiro': f"{agrupados['DINHEIRO']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'outros': f"{agrupados['OUTROS']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'total': f"{total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        }
        
        return jsonify({
            'success': True,
            'data': formatted_result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
