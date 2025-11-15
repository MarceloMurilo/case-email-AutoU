# 📧 Email Leitor - Classificador Inteligente de Emails

Aplicação web que classifica emails automaticamente em **PRODUTIVO** ou **IMPRODUTIVO** usando IA (OpenAI GPT), e gera respostas automáticas sugeridas.

## 🎯 Funcionalidades

- ✅ Upload de arquivos `.txt` ou `.pdf`
- ✅ Cola de texto manual
- ✅ Classificação automática por IA
- ✅ Geração de resposta inteligente
- ✅ Interface moderna e responsiva
- ✅ Deploy simples (Render + Netlify/Vercel)

## 🛠 Tecnologias

**Backend:**
- FastAPI (Python)
- OpenAI GPT-3.5-turbo
- pdfplumber para extração de PDF

**Frontend:**
- HTML5 / CSS3 / JavaScript Vanilla
- Design limpo e profissional

## 📁 Estrutura do Projeto

```
/backend
  ├── main.py           # API FastAPI
  ├── utils.py          # Funções auxiliares (LLM, extração)
  └── requirements.txt  # Dependências Python

/frontend
  ├── index.html        # Interface principal
  ├── style.css         # Estilos
  └── script.js         # Lógica do frontend

README.md
```

## 🚀 Como Rodar Localmente

### 1. Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar API Key da OpenAI
# Windows:
set OPENAI_API_KEY=sua-chave-aqui
# Linux/Mac:
export OPENAI_API_KEY=sua-chave-aqui

# Rodar servidor
python main.py
```

Backend estará rodando em: `http://localhost:8000`

### 2. Frontend

Opção 1 - Abrir diretamente:
```bash
# Abrir index.html no navegador
```

Opção 2 - Servidor local (recomendado):
```bash
cd frontend

# Python 3
python -m http.server 3000

# Ou use Live Server no VS Code
```

Frontend estará em: `http://localhost:3000`

## 🌐 Deploy em Produção

### Backend no Render

1. Crie conta em [render.com](https://render.com)
2. Crie novo **Web Service**
3. Conecte seu repositório GitHub
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Adicione variável de ambiente:
   - `OPENAI_API_KEY`: sua chave da OpenAI
6. Deploy!

URL do backend será algo como: `https://seu-app.onrender.com`

### Frontend no Netlify/Vercel

#### Netlify:

1. Crie conta em [netlify.com](https://netlify.com)
2. Arraste a pasta `/frontend` para o deploy
3. **IMPORTANTE:** Edite `script.js`:
   ```javascript
   const API_URL = 'https://seu-app.onrender.com'; // URL do seu backend
   ```
4. Deploy!

#### Vercel:

1. Crie conta em [vercel.com](https://vercel.com)
2. Importe repositório
3. Configure root como `/frontend`
4. Edite `API_URL` em `script.js` com URL do backend
5. Deploy!

## 🔑 Obtendo API Key da OpenAI

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie conta / faça login
3. Vá em **API Keys**
4. Crie nova chave
5. Copie e guarde com segurança

## 📋 Como Usar

1. Acesse a aplicação
2. **Opção 1:** Faça upload de arquivo `.txt` ou `.pdf`
   - **Opção 2:** Cole o texto do email manualmente
3. Clique em **Processar Email**
4. Veja os resultados:
   - **Categoria:** PRODUTIVO ou IMPRODUTIVO
   - **Resposta Sugerida:** Gerada pela IA
   - **Texto Original:** Preview do email

## 🧪 Testar API Diretamente

```bash
# Testar endpoint raiz
curl http://localhost:8000/

# Testar classificação com texto
curl -X POST http://localhost:8000/processar-email \
  -F "texto=Olá, preciso de suporte urgente com meu pedido #1234"
```

## ⚙️ Configurações Adicionais

### Trocar modelo da OpenAI

Em `utils.py`, altere:
```python
model="gpt-3.5-turbo"  # ou gpt-4, gpt-4-turbo
```

### Alterar temperatura (criatividade)

```python
temperature=0.3  # 0 = determinístico, 1 = criativo
```

## 🐛 Troubleshooting

**Erro de CORS:**
- Certifique-se que o backend tem CORS configurado corretamente

**API Key inválida:**
- Verifique se a variável `OPENAI_API_KEY` está configurada

**Erro ao extrair PDF:**
- Teste com arquivo PDF simples primeiro
- Alguns PDFs com imagens podem falhar

**Frontend não conecta ao backend:**
- Verifique se `API_URL` em `script.js` está correto
- Teste backend diretamente via curl

## 📝 Exemplos de Emails

### Produtivo:
```
Prezados,

Gostaria de solicitar suporte para o pedido #1234 que ainda não foi entregue.
Podem verificar o status?

Obrigado.
```

### Improdutivo:
```
Olá equipe,

Parabéns pelo excelente trabalho! Feliz aniversário da empresa!

Abraços.
```

## 📄 Licença

Projeto livre para uso educacional e comercial.

## 👨‍💻 Autor

**Marcelo Murilo Dantas**

Desenvolvido como case técnico de classificação de emails com IA.

---

**Dúvidas?** Consulte a documentação do FastAPI e OpenAI.


