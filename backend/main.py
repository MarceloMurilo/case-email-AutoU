from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import time

# Importar funções comuns
from utils_common import extract_text_from_pdf, extract_text_from_txt, clean_text

# Importar funções NLP (rápido/gratuito)
from utils_nlp import classify_email_nlp, generate_reply_nlp

# Importar funções Semânticas (MiniLM - gratuito/inteligente)
from utils_semantic import classify_email_semantic, generate_reply_semantic

# Importar funções LLM (inteligente/pago)
from utils_llm import classify_email_llm, generate_reply_llm

app = FastAPI(title="Email Leitor API")

# CORS para permitir frontend acessar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "API funcionando", "message": "Email Leitor API está online"}

@app.post("/processar-email")
async def processar_email(
    arquivo: Optional[UploadFile] = File(None),
    texto: Optional[str] = Form(None),
    modo: Optional[str] = Form("inteligente")
):
    """
    Processa email via arquivo (.txt ou .pdf) ou texto direto.
    Modos: 'rapido' (NLP), 'semantico' (MiniLM), 'inteligente' (LLM)
    Retorna: categoria e resposta automática.
    """
    
    # Validação: deve ter arquivo OU texto
    if not arquivo and not texto:
        raise HTTPException(status_code=400, detail="Envie um arquivo ou texto")
    
    email_text = ""
    
    # Processar arquivo
    if arquivo:
        filename = arquivo.filename.lower()
        content = await arquivo.read()
        
        if filename.endswith('.pdf'):
            email_text = extract_text_from_pdf(content)
        elif filename.endswith('.txt'):
            email_text = extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado. Use .txt ou .pdf")
    
    # Processar texto direto
    elif texto:
        email_text = texto
    
    # Limpeza do texto
    email_text = clean_text(email_text)
    
    if not email_text.strip():
        raise HTTPException(status_code=400, detail="Texto vazio ou não extraído")
    
    # Medir tempo
    start_time = time.time()
    
    # Processar de acordo com o modo
    if modo == "rapido":
        # Modo Rápido: NLP tradicional (gratuito)
        resultado = classify_email_nlp(email_text)
        categoria = resultado["categoria"]
        resposta = generate_reply_nlp(email_text, categoria)
        
        tempo_processamento = time.time() - start_time
        
        return {
            "categoria": categoria,
            "resposta": resposta,
            "texto_original": email_text[:500] + ("..." if len(email_text) > 500 else ""),
            "modo": "⚡ Rápido (NLP)",
            "tempo": f"{tempo_processamento:.2f}s",
            "custo": "Gratuito",
            "analise_nlp": resultado["analise"],
            "confianca": f"{resultado['confianca']}%"
        }
    
    elif modo == "semantico":
        # Modo Semântico: MiniLM (gratuito + inteligente)
        resultado = classify_email_semantic(email_text)
        categoria = resultado["categoria"]
        resposta = generate_reply_semantic(email_text, categoria)
        
        tempo_processamento = time.time() - start_time
        
        return {
            "categoria": categoria,
            "resposta": resposta,
            "texto_original": email_text[:500] + ("..." if len(email_text) > 500 else ""),
            "modo": "🧠 Semântico (MiniLM)",
            "tempo": f"{tempo_processamento:.2f}s",
            "custo": "Gratuito",
            "analise_semantica": resultado["analise_semantica"],
            "confianca": resultado["confianca"]
        }
    
    else:
        # Modo Inteligente: LLM (pago mas preciso)
        categoria = classify_email_llm(email_text)
        resposta = generate_reply_llm(email_text, categoria)
        
        tempo_processamento = time.time() - start_time
        
        return {
            "categoria": categoria,
            "resposta": resposta,
            "texto_original": email_text[:500] + ("..." if len(email_text) > 500 else ""),
            "modo": "🎯 Inteligente (IA)",
            "tempo": f"{tempo_processamento:.2f}s",
            "custo": "~$0.002",
            "confianca": "95%+"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


