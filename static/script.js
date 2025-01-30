// Função para exibir mensagens de erro
function showError(message) {
    const errorElement = document.getElementById('error-message');
    errorElement.textContent = message;
}

// Função para carregar as movimentações
function fetchMovimentacoes() {
    fetch('http://localhost:5000/api/movimentacoes')  // Certifique-se de que a URL está correta
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar movimentações');
            }
            return response.json();
        })
        .then(data => {
            console.log("Movimentações recebidas:", data);  // Log para depuração
            displayMovimentacoes(data);  // Exibir as movimentações
        })
        .catch(error => {
            console.error('Erro:', error);  // Log do erro
            showError('Erro ao carregar as movimentações: ' + error.message);
        });
}

// Função para exibir as movimentações na tela
function displayMovimentacoes(data) {
    const listElement = document.getElementById('movimentacoes-list');
    listElement.innerHTML = '';  // Limpa a lista existente

    data.movimentacoes.forEach(movimentacao => {
        const listItem = document.createElement('li');
        // Formatar a data/hora de forma legível (se necessário)
        const formattedDate = new Date(movimentacao.data_hora).toLocaleString();  // Converter para formato local
        listItem.textContent = `Posição: ${movimentacao.posicao_movimentada}, Estado: ${movimentacao.estado_sensor}, Data e Hora: ${formattedDate}`;
        listElement.appendChild(listItem);
    });
}

// Chama a função para carregar as movimentações quando a página for carregada
document.addEventListener('DOMContentLoaded', fetchMovimentacoes);






