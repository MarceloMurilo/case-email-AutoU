// Configuração da API
// Detectar automaticamente se está em produção ou desenvolvimento
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'  // Desenvolvimento local
    : 'https://case-email-autou.onrender.com'; // Backend em produção (Render)

// Elementos DOM
const fileUpload = document.getElementById('file-upload');
const fileName = document.getElementById('file-name');
const textInput = document.getElementById('text-input');
const processBtn = document.getElementById('process-btn');
const resultsSection = document.getElementById('results');
const errorDiv = document.getElementById('error');
const uploadSection = document.querySelector('.upload-section');
const newAnalysisBtn = document.getElementById('new-analysis');

// Mostrar nome do arquivo selecionado
fileUpload.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
        textInput.value = ''; // Limpar textarea se arquivo foi selecionado
    } else {
        fileName.textContent = '';
    }
});

// Limpar arquivo se texto foi digitado
textInput.addEventListener('input', () => {
    if (textInput.value.trim()) {
        fileUpload.value = '';
        fileName.textContent = '';
    }
});

// Processar email
processBtn.addEventListener('click', async () => {
    hideError();
    
    // Validação
    const hasFile = fileUpload.files.length > 0;
    const hasText = textInput.value.trim();
    
    if (!hasFile && !hasText) {
        showError('Por favor, envie um arquivo ou cole o texto do email.');
        return;
    }
    
    // Preparar dados
    const formData = new FormData();
    
    if (hasFile) {
        formData.append('arquivo', fileUpload.files[0]);
    } else {
        formData.append('texto', textInput.value.trim());
    }
    
    // Adicionar modo selecionado
    const modoSelecionado = document.querySelector('input[name="modo"]:checked').value;
    formData.append('modo', modoSelecionado);
    
    // Mostrar loading
    processBtn.classList.add('loading');
    processBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/processar-email`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao processar email');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        showError(`Erro: ${error.message}`);
    } finally {
        processBtn.classList.remove('loading');
        processBtn.disabled = false;
    }
});

// Exibir resultados
function displayResults(data) {
    // Esconder seção de upload
    uploadSection.style.display = 'none';
    
    // Preencher stats
    document.getElementById('modo-usado').textContent = data.modo;
    document.getElementById('tempo').textContent = `⏱️ ${data.tempo}`;
    document.getElementById('custo').textContent = `💰 ${data.custo}`;
    
    // Preencher resultados
    const categoriaEl = document.getElementById('categoria');
    categoriaEl.textContent = data.categoria;
    categoriaEl.className = 'categoria-badge ' + data.categoria.toLowerCase();
    
    document.getElementById('resposta').textContent = data.resposta;
    document.getElementById('texto-original').textContent = data.texto_original;
    
    // Mostrar análise NLP se disponível
    const analiseNlpSection = document.getElementById('analise-nlp');
    if (data.analise_nlp) {
        const nlpDetails = document.getElementById('nlp-details');
        nlpDetails.innerHTML = `
            <strong>Total de palavras:</strong> ${data.analise_nlp.total_palavras}<br>
            <strong>Palavras relevantes:</strong> ${data.analise_nlp.palavras_filtradas}<br>
            <strong>Indicadores produtivos:</strong> ${data.analise_nlp.palavras_chave_produtivo}<br>
            <strong>Indicadores improdutivos:</strong> ${data.analise_nlp.palavras_chave_improdutivo}<br>
            <strong>Contém números:</strong> ${data.analise_nlp.tem_numero ? 'Sim' : 'Não'}<br>
            <strong>Tipo de pergunta:</strong> ${data.analise_nlp.tipo_pergunta}<br>
            <strong>Confiança:</strong> ${data.confianca}
        `;
        analiseNlpSection.classList.remove('hidden');
    } else {
        analiseNlpSection.classList.add('hidden');
    }

    // Mostrar análise Semântica se disponível
    const analiseSemanticaSection = document.getElementById('analise-semantica');
    if (data.analise_semantica) {
        const semanticDetails = document.getElementById('semantic-details');
        semanticDetails.innerHTML = `
            <strong>Similaridade Produtivo:</strong> ${data.analise_semantica.similaridade_produtivo}%<br>
            <strong>Similaridade Improdutivo:</strong> ${data.analise_semantica.similaridade_improdutivo}%<br>
            <strong>Diferença:</strong> ${data.analise_semantica.diferenca}%<br>
            <strong>Confiança:</strong> ${data.confianca}
        `;
        analiseSemanticaSection.classList.remove('hidden');
    } else {
        analiseSemanticaSection.classList.add('hidden');
    }
    
    // Mostrar resultados
    resultsSection.classList.remove('hidden');
}

// Nova análise
newAnalysisBtn.addEventListener('click', () => {
    // Limpar formulário
    fileUpload.value = '';
    fileName.textContent = '';
    textInput.value = '';
    
    // Mostrar upload section
    uploadSection.style.display = 'block';
    
    // Esconder resultados
    resultsSection.classList.add('hidden');
    
    // Esconder erro
    hideError();
});

// Mostrar erro
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(hideError, 5000);
}

// Esconder erro
function hideError() {
    errorDiv.classList.add('hidden');
}


