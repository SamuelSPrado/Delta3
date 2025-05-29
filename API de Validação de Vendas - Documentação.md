# API de Validação de Vendas - Documentação

## Visão Geral

Esta API foi desenvolvida para automatizar o processo de cruzamento e análise de dados de vendas, validando se todos os valores vendidos pelo cliente estão corretos em todas as estruturas disponíveis. A API compara dados de três fontes diferentes:

1. **PEDIDO POS** (Transações Online e Offline do banco de dados)
2. **INVOICE ORDER** (Registros de faturamento do banco de dados)
3. **SIMPLE SALES API** (Dados de vendas da API externa)

## Estrutura do Projeto

O projeto foi estruturado de forma modular para facilitar a manutenção e reutilização:

```
validacao_vendas_api/
├── api/                    # Módulo de rotas da API
│   ├── __init__.py
│   └── routes.py           # Endpoints da API
├── models/                 # Módulo de modelos
│   ├── __init__.py
│   └── validator.py        # Lógica de validação e cruzamento
├── utils/                  # Módulo de utilidades
│   ├── __init__.py
│   └── formatters.py       # Funções para formatação de dados
└── app.py                  # Ponto de entrada da aplicação
```

## Endpoints da API

### 1. Obter Informações do Caixa

**Endpoint:** `/api/cashier/<caixa_id>`

**Método:** GET

**Descrição:** Obtém as datas de início e fim do caixa especificado.

**Parâmetros de URL:**
- `caixa_id` (string): ID do caixa

**Resposta de Sucesso:**
```json
{
  "id": "972ae953-ede0-4719-ae31-ec777989c735",
  "start_date": "2025-05-12T09:58:26.88",
  "end_date": "2025-05-12T22:09:52.003",
  "formatted_dates": "[2025-05-12][09:58:26.88] - [2025-05-12][22:09:52.003]"
}
```

**Resposta de Erro:**
```json
{
  "error": "ID do caixa não informado"
}
```

### 2. Validar Vendas

**Endpoint:** `/api/validate-sales`

**Método:** POST

**Descrição:** Valida as vendas entre as três estruturas (PEDIDO POS, INVOICE ORDER e SIMPLE SALES API).

**Corpo da Requisição:**
```json
{
  "local_id": "AAF9C6A6-90DC-F455-9558-7FDECF8AE2B1",
  "caixa_id": "972ae953-ede0-4719-ae31-ec777989c735",
  "start_date": "2025-05-12T09:58:26.88",
  "end_date": "2025-05-12T22:09:52.003"
}
```

**Resposta de Sucesso:**
```json
{
  "PEDIDO POS": {
    "débito": "1.234,56",
    "crédito": "2.345,67",
    "dinheiro": "345,78",
    "outros": "567,89",
    "total": "4.493,90"
  },
  "INVOICE ORDER": {
    "débito": "1.234,56",
    "crédito": "2.345,67",
    "dinheiro": "345,78",
    "outros": "567,89",
    "total": "4.493,90"
  },
  "SIMPLE SALES API": {
    "débito": "4,50",
    "crédito": "0,00",
    "dinheiro": "0,00",
    "outros": "0,00",
    "total": "4,50"
  }
}
```

**Resposta de Erro:**
```json
{
  "error": "Todos os campos são obrigatórios: local_id, caixa_id, start_date, end_date"
}
```

## Implementação de Autenticação

A API foi projetada para permitir que você implemente sua própria autenticação no backend. Aqui estão algumas orientações para implementar autenticação:

### 1. Autenticação MFA para SQL Server

Para implementar a autenticação MFA com SQL Server, você precisará modificar o arquivo `models/validator.py` para incluir sua lógica de autenticação. Aqui está um exemplo de como você pode implementar:

```python
import pyodbc

def connect_to_database(server, database, username):
    """
    Estabelece conexão com o banco de dados usando autenticação MFA.
    
    Args:
        server (str): Nome do servidor SQL.
        database (str): Nome do banco de dados.
        username (str): Nome de usuário para autenticação MFA.
        
    Returns:
        pyodbc.Connection: Objeto de conexão com o banco de dados.
    """
    try:
        # Configuração da string de conexão para autenticação MFA
        conn_str = (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            f"Authentication=ActiveDirectoryInteractive;"
            f"UID={username};"
        )
        
        # Estabelece a conexão
        connection = pyodbc.connect(conn_str)
        return connection
    
    except Exception as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")
```

### 2. Autenticação para APIs Externas

Para implementar a autenticação com APIs externas, você precisará modificar os métodos `get_cashier_dates` e `get_simple_sales` no arquivo `models/validator.py`. Aqui está um exemplo:

```python
def get_cashier_dates(self, caixa_id):
    """
    Obtém as datas de início e fim do caixa.
    """
    try:
        url = f"{self.base_url}/third/cashier/v1/{caixa_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer YOUR_API_KEY"  # Adicione sua chave de API aqui
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        cashier_info = response.json()
        
        # Resto do código...
    
    except Exception as e:
        raise Exception(f"Erro ao obter datas do caixa: {str(e)}")
```

### 3. Segurança Adicional

Para aumentar a segurança da sua API, considere implementar:

1. **JWT (JSON Web Tokens)**: Para autenticação entre seu frontend e esta API
2. **Rate Limiting**: Para prevenir abusos da API
3. **HTTPS**: Sempre use HTTPS em produção
4. **Validação de Entrada**: Valide todos os dados de entrada para prevenir injeções

## Implementação das Consultas SQL

Para implementar as consultas SQL reais, você precisará modificar o método `validate_sales` no arquivo `models/validator.py`. Aqui está um exemplo:

```python
def validate_sales(self, local_id, caixa_id, start_date, end_date):
    """
    Valida as vendas entre as três estruturas.
    """
    try:
        # Conectar ao banco de dados
        connection = connect_to_database(server, database, username)
        
        # Executar consulta para PEDIDO POS (Transação Offline)
        offline_query = """
        SELECT 
            FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 1 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'CRÉDITO [NT]',
            FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 2 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DÉBITO [NT]',
            FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 3 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DINHEIRO',
            FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO NOT IN (1, 2, 3) THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'OUTROS',
            FORMAT(SUM(PP.DESCONTO), 'N', 'PT-BR') AS 'DESCONTO',
            FORMAT(SUM(T.VALOR), 'N', 'PT-BR') AS 'TOTAL TRANSAÇÃO OFFLINE'
        FROM 
            VWTRANSACAOOFFLINE T 
            JOIN VWPEDIDOPOS PP ON T.PEDIDOPOSID = PP.ID
        WHERE
            T.LOCALCLIENTEID = ?
            AND PP.SESSAOPOSID = ?
            AND T.STATUS NOT IN (5)
        """
        
        # Executar outras consultas...
        
        # Processar resultados...
        
        # Fechar conexão
        connection.close()
        
        # Retornar resultados
        return results
    
    except Exception as e:
        raise Exception(f"Erro durante a validação de vendas: {str(e)}")
```

## Executando a API

Para executar a API localmente:

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

## Integrando com Frontend

Para integrar esta API com seu frontend, você pode fazer requisições HTTP para os endpoints fornecidos. Aqui está um exemplo usando JavaScript:

```javascript
// Exemplo de obtenção de datas do caixa
async function getCashierDates(caixaId) {
    try {
        const response = await fetch(`http://localhost:5000/api/cashier/${caixaId}`);
        if (!response.ok) {
            throw new Error('Erro ao obter datas do caixa');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
    }
}

// Exemplo de validação de vendas
async function validateSales(localId, caixaId, startDate, endDate) {
    try {
        const response = await fetch('http://localhost:5000/api/validate-sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                local_id: localId,
                caixa_id: caixaId,
                start_date: startDate,
                end_date: endDate
            })
        });
        if (!response.ok) {
            throw new Error('Erro ao validar vendas');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
    }
}
```
