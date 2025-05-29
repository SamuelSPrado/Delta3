// Script para integração com o backend Flask
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const localIdInput = document.getElementById('localId');
    const caixaIdInput = document.getElementById('caixaId');
    const btnPesquisarCaixa = document.getElementById('btnPesquisarCaixa');
    const btnAnalisarInvoice = document.getElementById('btnAnalisarInvoice');
    const btnAnalisarPedido = document.getElementById('btnAnalisarPedido');
    const btnAnalisarAPI = document.getElementById('btnAnalisarAPI');
    
    // Elementos de resultado Invoice Order
    const invoiceDebito = document.getElementById('invoiceDebito');
    const invoiceCredito = document.getElementById('invoiceCredito');
    const invoiceDinheiro = document.getElementById('invoiceDinheiro');
    const invoiceOutros = document.getElementById('invoiceOutros');
    const invoiceTotal = document.getElementById('invoiceTotal');
    
    // Elementos de resultado Pedido Pos
    const pedidoDebito = document.getElementById('pedidoDebito');
    const pedidoCredito = document.getElementById('pedidoCredito');
    const pedidoDinheiro = document.getElementById('pedidoDinheiro');
    const pedidoOutros = document.getElementById('pedidoOutros');
    const pedidoTotal = document.getElementById('pedidoTotal');
    
    // Elementos de resultado Simple Sale API
    const apiDebito = document.getElementById('apiDebito');
    const apiCredito = document.getElementById('apiCredito');
    const apiDinheiro = document.getElementById('apiDinheiro');
    const apiOutros = document.getElementById('apiOutros');
    const apiTotal = document.getElementById('apiTotal');
    
    // Toast notification
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toastIcon');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const closeIcon = document.querySelector('.close');
    
    // Função para mostrar toast notification
    function showToast(type, title, message) {
        toast.className = 'toast';
        
        // Definir tipo de toast
        if (type === 'success') {
            toast.classList.add('success');
            toastIcon.className = 'fas fa-check-circle';
        } else if (type === 'error') {
            toast.classList.add('error');
            toastIcon.className = 'fas fa-exclamation-circle';
        } else if (type === 'warning') {
            toast.classList.add('warning');
            toastIcon.className = 'fas fa-exclamation-triangle';
        } else {
            toastIcon.className = 'fas fa-info-circle';
        }
        
        toastTitle.innerText = title;
        toastMessage.innerText = message;
        
        toast.classList.add('active');
        
        // Auto fechar após 5 segundos
        setTimeout(() => {
            toast.classList.remove('active');
        }, 5000);
    }
    
    // Fechar toast ao clicar no X
    closeIcon.addEventListener('click', () => {
        toast.classList.remove('active');
    });
    
    // Função para validar campos obrigatórios
    function validateRequiredFields() {
        const localId = localIdInput.value.trim();
        const caixaId = caixaIdInput.value.trim();
        
        if (!localId || !caixaId) {
            showToast('warning', 'Campos obrigatórios', 'Preencha LOCAL_ID e CAIXA_ID para continuar.');
            return false;
        }
        
        return true;
    }
    
    // Função para adicionar/remover classe de loading
    function toggleLoading(button, isLoading) {
        if (isLoading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }
    
    // Evento de clique no botão Pesquisar Caixa
    btnPesquisarCaixa.addEventListener('click', function() {
        const caixaId = caixaIdInput.value.trim();
        
        if (!caixaId) {
            showToast('warning', 'Campo obrigatório', 'Informe o CAIXA_ID para pesquisar.');
            return;
        }
        
        toggleLoading(btnPesquisarCaixa, true);
        
        // Requisição para obter datas do caixa
        fetch(`/api/cashier/${caixaId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('success', 'Caixa encontrado', `Datas do caixa: ${data.start} até ${data.end}`);
                } else {
                    showToast('error', 'Erro', data.error);
                }
                toggleLoading(btnPesquisarCaixa, false);
            })
            .catch(error => {
                showToast('error', 'Erro de conexão', 'Não foi possível conectar ao servidor.');
                console.error('Erro:', error);
                toggleLoading(btnPesquisarCaixa, false);
            });
    });
    
    // Evento de clique no botão Analisar Invoice
    btnAnalisarInvoice.addEventListener('click', function() {
        if (!validateRequiredFields()) return;
        
        toggleLoading(btnAnalisarInvoice, true);
        
        // Requisição para analisar Invoice Order
        fetch('/api/invoice-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                local_id: localIdInput.value.trim(),
                caixa_id: caixaIdInput.value.trim()
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Atualizar resultados na interface
                    invoiceDebito.textContent = data.data.debito;
                    invoiceCredito.textContent = data.data.credito;
                    invoiceDinheiro.textContent = data.data.dinheiro;
                    invoiceOutros.textContent = data.data.outros;
                    invoiceTotal.textContent = data.data.total;
                    
                    showToast('success', 'Invoice Order', 'Análise concluída com sucesso!');
                } else {
                    showToast('error', 'Erro', data.error);
                }
                toggleLoading(btnAnalisarInvoice, false);
            })
            .catch(error => {
                showToast('error', 'Erro de conexão', 'Não foi possível conectar ao servidor.');
                console.error('Erro:', error);
                toggleLoading(btnAnalisarInvoice, false);
            });
    });
    
    // Evento de clique no botão Analisar Pedido
    btnAnalisarPedido.addEventListener('click', function() {
        if (!validateRequiredFields()) return;
        
        toggleLoading(btnAnalisarPedido, true);
        
        // Requisição para analisar Pedido POS
        fetch('/api/pedido-pos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                local_id: localIdInput.value.trim(),
                caixa_id: caixaIdInput.value.trim()
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Calcular valores combinados (online + offline)
                    const online = data.data.online;
                    const offline = data.data.offline;
                    
                    // Atualizar resultados na interface
                    pedidoDebito.textContent = `${offline.debito} + ${online.debito}`;
                    pedidoCredito.textContent = `${offline.credito} + ${online.credito}`;
                    pedidoDinheiro.textContent = `${offline.dinheiro} + ${online.dinheiro}`;
                    pedidoOutros.textContent = `${offline.outros} + ${online.outros}`;
                    pedidoTotal.textContent = `${offline.total} + ${online.total}`;
                    
                    showToast('success', 'Pedido POS', 'Análise concluída com sucesso!');
                } else {
                    showToast('error', 'Erro', data.error);
                }
                toggleLoading(btnAnalisarPedido, false);
            })
            .catch(error => {
                showToast('error', 'Erro de conexão', 'Não foi possível conectar ao servidor.');
                console.error('Erro:', error);
                toggleLoading(btnAnalisarPedido, false);
            });
    });
    
    // Evento de clique no botão Analisar API
    btnAnalisarAPI.addEventListener('click', function() {
        if (!validateRequiredFields()) return;
        
        toggleLoading(btnAnalisarAPI, true);
        
        // Requisição para analisar Simple Sales API
        fetch('/api/simple-sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                local_id: localIdInput.value.trim(),
                caixa_id: caixaIdInput.value.trim()
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Atualizar resultados na interface
                    apiDebito.textContent = data.data.debito;
                    apiCredito.textContent = data.data.credito;
                    apiDinheiro.textContent = data.data.dinheiro;
                    apiOutros.textContent = data.data.outros;
                    apiTotal.textContent = data.data.total;
                    
                    showToast('success', 'Simple Sales API', 'Análise concluída com sucesso!');
                } else {
                    showToast('error', 'Erro', data.error);
                }
                toggleLoading(btnAnalisarAPI, false);
            })
            .catch(error => {
                showToast('error', 'Erro de conexão', 'Não foi possível conectar ao servidor.');
                console.error('Erro:', error);
                toggleLoading(btnAnalisarAPI, false);
            });
    });
    
    // Função para comparar resultados e destacar diferenças
    function highlightDifferences() {
        // Implementação futura para destacar diferenças entre os resultados
    }
});
