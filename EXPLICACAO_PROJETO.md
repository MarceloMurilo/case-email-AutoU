# 📧 Explicação do Projeto - Email Leitor

## 🎯 **O que o projeto faz?**

Sistema web que **classifica emails automaticamente** em **PRODUTIVO** ou **IMPRODUTIVO** e **gera respostas automáticas sugeridas** usando Inteligência Artificial.

### Exemplos:
- **PRODUTIVO**: "Preciso de suporte urgente com meu pedido #1234"
- **IMPRODUTIVO**: "Parabéns pelo excelente trabalho! Feliz aniversário!"

---

## 🏗️ **Arquitetura do Projeto**

### **Frontend** (Interface do Usuário)
- **Localização**: `/frontend/`
- **Tecnologias**: HTML5, CSS3, JavaScript (Vanilla)
- **Hospedagem**: Netlify

**Arquivos principais:**
- `index.html` - Estrutura da página (formulário, botões, resultados)
- `style.css` - Estilos visuais (cores, layout, responsividade)
- `script.js` - Lógica JavaScript (envio de dados, exibição de resultados)

**O que faz:**
1. Permite upload de arquivo `.txt` ou `.pdf`
2. Permite colar texto manualmente
3. Envia dados para o backend via API
4. Exibe resultados (categoria + resposta sugerida)

---

### **Backend** (API/Processamento)
- **Localização**: `/backend/`
- **Tecnologias**: Python, FastAPI
- **Hospedagem**: Render

**Arquivos principais:**

#### 1. `main.py` - API Principal
- Cria servidor FastAPI
- Configura CORS (permite frontend acessar)
- Endpoint `/` - Verifica se API está online
- Endpoint `/processar-email` - Processa email e retorna classificação

**Fluxo:**
```
1. Recebe arquivo OU texto do frontend
2. Extrai texto (se for PDF, usa pdfplumber)
3. Limpa o texto (remove espaços extras)
4. Escolhe modo de análise (Rápido, Semântico ou Inteligente)
5. Classifica email (PRODUTIVO ou IMPRODUTIVO)
6. Gera resposta automática
7. Retorna JSON com resultados
```

#### 2. `utils_common.py` - Funções Auxiliares
- `extract_text_from_pdf()` - Extrai texto de PDFs
- `extract_text_from_txt()` - Lê arquivos TXT
- `clean_text()` - Remove espaços extras e formata texto

#### 3. `utils_nlp.py` - Modo Rápido (NLP Tradicional)
- **Tecnologia**: NLTK + Scikit-learn
- **Custo**: Gratuito
- **Como funciona:**
  1. Tokeniza texto (divide em palavras)
  2. Remove stop words (palavras comuns como "o", "a", "de")
  3. Procura palavras-chave (ex: "suporte", "urgente" = PRODUTIVO)
  4. Conta indicadores produtivos vs improdutivos
  5. Classifica baseado em pontuação

#### 4. `utils_semantic.py` - Modo Semântico (Desabilitado)
- **Tecnologia**: Sentence Transformers (MiniLM)
- **Status**: Desabilitado no Render (biblioteca muito pesada)
- **Nota**: Faz fallback para modo NLP quando não disponível

#### 5. `utils_llm.py` - Modo Inteligente (IA)
- **Tecnologia**: OpenAI GPT-3.5-turbo
- **Custo**: ~$0.002 por email
- **Como funciona:**
  1. Envia texto para API da OpenAI
  2. Usa prompt especializado para classificação
  3. IA entende contexto, negações, ironia
  4. Gera resposta personalizada e natural

---

## 🔄 **Fluxo Completo de Funcionamento**

```
┌─────────────┐
│   Usuário   │
│  (Frontend) │
└──────┬──────┘
       │
       │ 1. Upload arquivo OU cola texto
       │ 2. Seleciona modo (Rápido ou Inteligente)
       │ 3. Clica em "Processar Email"
       │
       ▼
┌─────────────────────────────────┐
│      script.js (Frontend)       │
│  - Valida entrada               │
│  - Cria FormData                │
│  - Envia POST para backend      │
└──────────────┬──────────────────┘
               │
               │ HTTP POST
               │ /processar-email
               │
               ▼
┌─────────────────────────────────┐
│     main.py (Backend)           │
│  - Recebe arquivo/texto         │
│  - Extrai texto (PDF/TXT)       │
│  - Limpa texto                  │
└──────────────┬──────────────────┘
               │
               │ Escolhe modo
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌─────────────┐  ┌─────────────┐
│ Modo Rápido │  │ Modo        │
│ (NLP)       │  │ Inteligente │
│             │  │ (OpenAI)    │
│ utils_nlp   │  │ utils_llm   │
└──────┬──────┘  └──────┬──────┘
       │                │
       │ Classifica     │ Classifica
       │ email          │ email
       │                │
       └────────┬───────┘
                │
                ▼
       ┌─────────────────┐
       │ Gera Resposta   │
       │ Automática      │
       └────────┬────────┘
                │
                │ JSON Response
                │
                ▼
┌─────────────────────────────────┐
│      script.js (Frontend)       │
│  - Recebe JSON                   │
│  - Exibe categoria               │
│  - Exibe resposta sugerida       │
│  - Mostra estatísticas           │
└─────────────────────────────────┘
```

---

## 🎨 **Modos de Análise Disponíveis**

### ⚡ **Modo Rápido (NLP)**
- **Tecnologia**: NLTK + Regras
- **Custo**: Gratuito
- **Velocidade**: Muito rápida (~0.1s)
- **Precisão**: Boa para casos simples
- **Como funciona**: Análise de palavras-chave e padrões

### 🎯 **Modo Inteligente (IA)**
- **Tecnologia**: OpenAI GPT-3.5-turbo
- **Custo**: ~$0.002 por email
- **Velocidade**: Rápida (~1-2s)
- **Precisão**: Excelente (entende contexto, ironia, negações)
- **Como funciona**: IA analisa significado completo do texto

### 🧠 **Modo Semântico** (Desabilitado)
- **Status**: Indisponível no Render (biblioteca muito pesada)
- **Nota**: Faz fallback automático para modo NLP

---

## 📦 **Dependências Principais**

### Backend (`requirements.txt`):
- `fastapi` - Framework web (API)
- `uvicorn` - Servidor ASGI
- `openai` - Cliente OpenAI (modo inteligente)
- `pdfplumber` - Extração de texto de PDFs
- `nltk` - Processamento de linguagem natural
- `scikit-learn` - Machine learning (análise NLP)

### Frontend:
- Nenhuma dependência externa (JavaScript puro)

---

## 🌐 **Deploy**

### Backend (Render):
- **URL**: `https://case-email-autou.onrender.com`
- **Configuração**:
  - Root Directory: `backend`
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Variável de ambiente: `OPENAI_API_KEY`

### Frontend (Netlify):
- **URL**: `https://email-autou.netlify.app`
- **Configuração**:
  - Base Directory: `frontend`
  - Build: (vazio - HTML estático)
  - Publish: (vazio)

---

## 🔑 **Pontos Importantes**

1. **CORS**: Backend permite requisições de qualquer origem (`allow_origins=["*"]`)

2. **Extração de PDF**: Usa `pdfplumber` para extrair texto de PDFs

3. **Fallback**: Modo semântico automaticamente usa NLP quando não disponível

4. **Detecção de Ambiente**: Frontend detecta automaticamente se está em localhost ou produção

5. **Validação**: Backend valida se tem arquivo OU texto antes de processar

---

## 📊 **Estrutura de Resposta da API**

```json
{
  "categoria": "PRODUTIVO",
  "resposta": "Olá!\n\nRecebemos sua solicitação...",
  "texto_original": "Preciso de suporte...",
  "modo": "⚡ Rápido (NLP)",
  "tempo": "0.15s",
  "custo": "Gratuito",
  "confianca": "85%",
  "analise_nlp": {
    "total_palavras": 25,
    "palavras_filtradas": 15,
    "palavras_chave_produtivo": 3,
    "palavras_chave_improdutivo": 0
  }
}
```

---

## 🎯 **Resumo Técnico**

**Frontend**: Interface simples que envia dados e exibe resultados  
**Backend**: API que processa texto, classifica emails e gera respostas  
**IA**: Usa OpenAI GPT para análise inteligente (modo premium)  
**NLP**: Usa NLTK para análise rápida baseada em regras (modo gratuito)  
**Deploy**: Render (backend) + Netlify (frontend)

---

**Desenvolvido por: Marcelo Murilo Dantas**

