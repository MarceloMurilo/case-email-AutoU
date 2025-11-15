"""
NLP Tradicional - Modo Rápido (Gratuito)
Classificação baseada em regras, palavras-chave e heurísticas
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Baixar recursos NLTK (executar apenas uma vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def classify_email_nlp(text: str) -> dict:
    """
    Modo RÁPIDO: Classificação usando NLP tradicional (gratuito)
    Retorna categoria e análise NLP
    """
    # Processar texto com NLP
    text_lower = text.lower()
    
    # Tokenizar
    tokens = word_tokenize(text_lower, language='portuguese')
    
    # Remover stop words
    stop_words = set(stopwords.words('portuguese'))
    tokens_filtrados = [w for w in tokens if w.isalnum() and w not in stop_words]
    
    # Palavras-chave que indicam email PRODUTIVO
    keywords_produtivo = [
        'suporte', 'ajuda', 'problema', 'erro', 'urgente', 'preciso',
        'solicito', 'dúvida', 'questão', 'pedido', 'status', 'atualização',
        'informação', 'como', 'quando', 'onde', 'resolver', 'solução',
        'não', 'funciona', 'conseguir', 'tentar', 'tentando'
    ]
    
    # Palavras-chave que indicam email IMPRODUTIVO
    keywords_improdutivo = [
        'parabéns', 'felicitações', 'aniversário', 'obrigado', 'obrigada',
        'agradecimento', 'feliz', 'natal', 'ano', 'novo', 'sucesso',
        'congratulações', 'festa', 'comemoração', 'celebração'
    ]
    
    # Contar matches
    score_produtivo = sum(1 for k in keywords_produtivo if k in text_lower)
    score_improdutivo = sum(1 for k in keywords_improdutivo if k in text_lower)
    
    # Heurísticas adicionais
    tem_numero = bool(re.search(r'\d+', text))
    tem_interrogacao = '?' in text
    tem_exclamacao_multipla = '!!' in text or '!!!' in text
    
    # Analisar tipo de pergunta (mais específico)
    perguntas_produtivas = [
        'como', 'quando', 'onde', 'qual', 'quais', 'porque', 'por que',
        'quanto', 'quem', 'posso', 'pode', 'consigo', 'consegue',
        'existe', 'tem como', 'é possível', 'funciona', 'fazer'
    ]
    
    perguntas_superficiais = [
        'tudo bem', 'como vai', 'beleza', 'e aí', 'tá bom',
        'legal', 'show', 'massa', 'dando role', 'suave'
    ]
    
    # Verificar se é pergunta produtiva ou superficial
    eh_pergunta_produtiva = tem_interrogacao and any(p in text_lower for p in perguntas_produtivas)
    eh_pergunta_superficial = tem_interrogacao and any(p in text_lower for p in perguntas_superficiais)
    
    # Ajustar scores
    if tem_numero:
        score_produtivo += 2  # Números são fortes indicadores (pedido #123)
    
    if eh_pergunta_produtiva:
        score_produtivo += 2  # Pergunta genuína
    elif tem_interrogacao and not eh_pergunta_superficial:
        score_produtivo += 1  # Pergunta genérica (neutro)
    
    if eh_pergunta_superficial:
        score_improdutivo += 1  # Pergunta social
    
    if tem_exclamacao_multipla and score_improdutivo > 0:
        score_improdutivo += 1
    
    # Decidir categoria
    # Regra especial: textos muito curtos (< 3 palavras) sem contexto claro
    if len(tokens_filtrados) < 3 and score_produtivo <= 1 and score_improdutivo == 0:
        categoria = "IMPRODUTIVO"  # Texto muito curto/vago
    elif score_produtivo > score_improdutivo:
        categoria = "PRODUTIVO"
    elif score_improdutivo > score_produtivo:
        categoria = "IMPRODUTIVO"
    else:
        # Empate: usar tamanho (emails longos tendem a ser produtivos)
        categoria = "PRODUTIVO" if len(tokens_filtrados) > 15 else "IMPRODUTIVO"
    
    # Análise NLP
    tipo_pergunta = "Nenhuma"
    if eh_pergunta_produtiva:
        tipo_pergunta = "Produtiva (como/quando/onde)"
    elif eh_pergunta_superficial:
        tipo_pergunta = "Social (tudo bem?)"
    elif tem_interrogacao:
        tipo_pergunta = "Genérica"
    
    analise = {
        "total_palavras": len(tokens),
        "palavras_filtradas": len(tokens_filtrados),
        "palavras_chave_produtivo": score_produtivo,
        "palavras_chave_improdutivo": score_improdutivo,
        "tem_numero": tem_numero,
        "tem_pergunta": tem_interrogacao,
        "tipo_pergunta": tipo_pergunta
    }
    
    return {
        "categoria": categoria,
        "analise": analise,
        "confianca": max(score_produtivo, score_improdutivo) * 10  # 0-100%
    }


def generate_reply_nlp(text: str, categoria: str) -> str:
    """
    Modo RÁPIDO: Resposta template (gratuito)
    """
    if categoria == "PRODUTIVO":
        return """Olá!

Obrigado por entrar em contato. Recebemos sua mensagem e nossa equipe está analisando sua solicitação.

Retornaremos em breve com uma resposta detalhada.

Atenciosamente,
Equipe de Suporte"""
    else:
        return """Olá!

Muito obrigado pela sua mensagem!

Ficamos felizes com seu contato.

Atenciosamente,
Equipe"""


