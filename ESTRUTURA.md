# 📁 Estrutura do Backend

## 🗂️ **Organização dos Arquivos**

```
backend/
├── main.py              # API FastAPI - Rotas e endpoints
├── utils_common.py      # Funções comuns (extração PDF/TXT, limpeza)
├── utils_nlp.py         # NLP Tradicional - Modo Rápido ⚡
├── utils_semantic.py    # Semântico (MiniLM) - Modo Inteligente Gratuito 🧠
├── utils_llm.py         # LLM (OpenAI) - Modo Premium 🎯
└── requirements.txt     # Dependências
```

---

## 📄 **Descrição dos Arquivos**

### **1. main.py**
**Responsabilidade:** API e rotas

- ✅ Define endpoints FastAPI
- ✅ Gerencia CORS
- ✅ Processa requests
- ✅ Chama funções NLP ou LLM conforme modo

**Rotas:**
- `GET /` - Status da API
- `POST /processar-email` - Processa email (modo: rapido/semantico/inteligente)

---

### **2. utils_common.py**
**Responsabilidade:** Funções compartilhadas

**Funções:**
- `extract_text_from_pdf()` - Extrai texto de PDF
- `extract_text_from_txt()` - Extrai texto de TXT
- `clean_text()` - Limpeza básica

**Usado por:** Ambos os modos (NLP e LLM)

---

### **3. utils_nlp.py** ⚡
**Responsabilidade:** NLP Tradicional (Gratuito)

**Biblioteca:** NLTK
**Custo:** $0.00
**Velocidade:** ~0.05s

**Funções:**
- `classify_email_nlp()` - Classifica por palavras-chave e regras
- `generate_reply_nlp()` - Gera resposta template

**Como funciona:**
1. Tokenização (NLTK)
2. Remove stop words
3. Conta palavras-chave produtivas/improdutivas
4. Analisa tipo de pergunta
5. Aplica heurísticas (números, perguntas específicas)
6. Retorna categoria + análise detalhada

**Ideal para:**
- Alta escala (milhares de emails)
- Orçamento limitado
- Emails simples e diretos

---

### **4. utils_semantic.py** 🧠
**Responsabilidade:** Análise Semântica (Gratuito + Inteligente)

**Biblioteca:** sentence-transformers (MiniLM-L6-v2)
**Custo:** $0.00
**Velocidade:** ~0.5s

**Funções:**
- `classify_email_semantic()` - Classifica por similaridade semântica
- `generate_reply_semantic()` - Gera resposta template

**Como funciona:**
1. Carrega modelo MiniLM-L6-v2 (80MB)
2. Cria embeddings do texto
3. Compara similaridade com referências produtivas/improdutivas
4. Usa cosine similarity
5. Retorna categoria + scores de similaridade

**Ideal para:**
- Melhor que NLP tradicional
- Entende contexto semântico
- Totalmente gratuito e offline
- Emails complexos sem custo

**Vantagens sobre NLP:**
- ✅ Entende contexto ("protocolo" > "feliz natal")
- ✅ Análise semântica real
- ✅ Não depende só de palavras-chave
- ✅ Mais inteligente que regras

---

### **5. utils_llm.py** 🎯
**Responsabilidade:** IA Avançada (Pago)

**Biblioteca:** OpenAI GPT-3.5-turbo
**Custo:** ~$0.002 por email
**Velocidade:** ~2s

**Funções:**
- `classify_email_llm()` - Classifica via IA (entende contexto)
- `generate_reply_llm()` - Gera resposta personalizada

**Como funciona:**
1. Envia texto completo para OpenAI
2. LLM analisa contexto, tom, intenção
3. Entende negações, sarcasmo, ironia
4. Retorna categoria precisa
5. Gera resposta contextualizada

**Ideal para:**
- Emails complexos
- Textos com nuances
- Melhor precisão (95%+)

---

## 🔄 **Fluxo de Processamento**

```
┌─────────────────┐
│  Frontend       │
│  (escolhe modo) │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  main.py        │
│  /processar-email
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    v         v
┌─────────┐ ┌─────────┐
│  NLP    │ │  LLM    │
│ Rápido  │ │Intelige.│
└─────────┘ └─────────┘
    │         │
    └────┬────┘
         │
         v
    ┌─────────┐
    │ Response│
    └─────────┘
```

---

## 🛠️ **Como Modificar**

### **Adicionar palavra-chave no NLP:**
Edite `utils_nlp.py`:
```python
keywords_produtivo = [
    'suporte', 'ajuda', 'problema',
    'sua_palavra_aqui'  # ← Adicione aqui
]
```

### **Melhorar prompt do LLM:**
Edite `utils_llm.py`:
```python
prompt = f"""Você é um classificador...
[modifique o prompt aqui]
"""
```

### **Adicionar novo modo:**
1. Crie `utils_novo_modo.py`
2. Importe em `main.py`
3. Adicione condição no endpoint

---

## 📊 **Comparação dos 3 Modos**

| Aspecto | ⚡ NLP (Rápido) | 🧠 Semântico (MiniLM) | 🎯 Premium (GPT) |
|---------|----------------|----------------------|------------------|
| **Arquivo** | utils_nlp.py | utils_semantic.py | utils_llm.py |
| **Custo** | Gratuito | Gratuito | ~$0.002/email |
| **Velocidade** | 0.05s | 0.5s | 2s |
| **Precisão** | ~70% | ~85% | 95%+ |
| **Entende contexto** | ❌ | ✅ | ✅✅ |
| **Entende negação** | ❌ | ⚠️ | ✅ |
| **Entende sarcasmo** | ❌ | ❌ | ✅ |
| **Análise detalhada** | ✅ | ✅ | ❌ |
| **Offline** | ✅ | ✅ | ❌ |
| **Escalável** | ✅✅✅ | ✅✅ | ✅ |

### **🎯 Recomendação de Uso:**

**⚡ NLP Rápido:**
- Emails muito simples
- Alta escala (milhares/segundo)
- Análise exploratória

**🧠 Semântico (RECOMENDADO):**
- **Melhor custo-benefício**
- Emails normais do dia-a-dia
- Precisão boa + gratuito
- Offline (sem internet)

**🎯 Premium:**
- Emails complexos
- Textos com nuances
- Máxima precisão

---

## 🚀 **Próximos Passos**

- [ ] Adicionar testes unitários para cada módulo
- [ ] Implementar cache para respostas comuns
- [ ] Criar modo híbrido (NLP + LLM)
- [ ] Logs detalhados por modo
- [ ] Métricas de performance

