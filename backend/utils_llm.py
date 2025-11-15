"""
LLM (IA) - Modo Inteligente (Pago)
Classificação e geração de respostas usando OpenAI GPT
"""
import os
from openai import OpenAI


# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_email_llm(text: str) -> str:
    """
    Modo INTELIGENTE: Classificação usando LLM (OpenAI)
    Entende contexto, negações, sarcasmo, ironia
    """
    prompt = f"""Você é um classificador de emails corporativos.
Classifique o email abaixo em:
- PRODUTIVO
- IMPRODUTIVO

Produtivo = exige ação, suporte, atualização, dúvida ou resposta de trabalho.
Improdutivo = agradecimentos, felicitações, parabéns, mensagens sociais, aniversários.

Email:
{text}

Responda somente com: PRODUTIVO ou IMPRODUTIVO."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador preciso de emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=50
        )
        
        categoria = response.choices[0].message.content.strip().upper()
        
        # Garantir que retorna uma das duas opções
        if "PRODUTIVO" in categoria and "IMPRODUTIVO" not in categoria:
            return "PRODUTIVO"
        elif "IMPRODUTIVO" in categoria:
            return "IMPRODUTIVO"
        else:
            return "IMPRODUTIVO"  # Default
            
    except Exception as e:
        print(f"Erro na classificação LLM: {str(e)}")
        return "PRODUTIVO"  # Fallback


def generate_reply_llm(text: str, categoria: str) -> str:
    """
    Modo INTELIGENTE: Resposta personalizada usando LLM (OpenAI)
    Gera resposta contextualizada e natural
    """
    prompt = f"""Gere uma resposta educada, curta e profissional com base no email abaixo.

Categoria: {categoria}

Regras:
- Se for PRODUTIVO: responda como atendimento.
- Se for IMPRODUTIVO: responda de forma simpática e curta.
- Não invente informações.
- Máximo de 2 parágrafos curtos.
- SEMPRE assine com "Equipe AutoU" no final. NUNCA use "[Seu Nome]", "[Nome]" ou qualquer placeholder.
- A resposta deve ser completa e pronta para enviar, sem placeholders.

Email:
{text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de email profissional da empresa AutoU. Sempre assine as respostas com 'Equipe AutoU'. Nunca use placeholders como [Seu Nome]."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Erro ao gerar resposta LLM: {str(e)}")
        
        # Fallback
        if categoria == "IMPRODUTIVO":
            return "Obrigado pela mensagem!"
        else:
            return "Obrigado! Estamos analisando sua solicitação e retornaremos em breve."


