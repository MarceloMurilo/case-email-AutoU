# utils_semantic.py
"""
Classificação Semântica usando MiniLM-L6-v2
Com detecção de negação e ajustes inteligentes

NOTA: Modo semântico disponível apenas em localhost (biblioteca muito pesada para Render).
Faz fallback para modo NLP quando sentence-transformers não está disponível ou em produção.
"""
import os

# Verificar se está em localhost (desenvolvimento)
IS_LOCALHOST = os.getenv("RENDER") is None  # Render define variável RENDER em produção

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    # Carregar modelo MiniLM apenas se estiver em localhost
    if IS_LOCALHOST:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        SEMANTIC_AVAILABLE = True
    else:
        SEMANTIC_AVAILABLE = False
        model = None
except ImportError:
    # Fallback: usar NLP quando sentence-transformers não está disponível
    SEMANTIC_AVAILABLE = False
    model = None

# Importar NLP para fallback
if not SEMANTIC_AVAILABLE:
    from utils_nlp import classify_email_nlp, generate_reply_nlp


# 🚫 Frases que anulam produtividade mesmo se o texto parecer técnico
NEGACOES = [
    "não precisa", "nao precisa",
    "não é necessário", "nao e necessario",
    "não necessita", "nao necessita",
    "pode desconsiderar", "podem desconsiderar",
    "já foi resolvido", "ja foi resolvido",
    "tudo certo por aqui",
    "nenhuma ação", "nenhuma acao",
    "não exige retorno", "nao exige retorno",
    "apenas registro", "só registro",
    "somente para informar", "apenas para informar"
]


# 📌 Referências ampliadas
REFERENCIAS = {
    "produtivo": [
        "protocolo",
        "número de chamado",
        "segue em anexo",
        "currículo",
        "documento",
        "pedido",
        "solicitação",
        "informações",
        "atualização",
        "necessário verificar",
        "urgente",
        "preciso de ajuda",
        "pode verificar",
        "erro no sistema",
        "chamado em aberto"
    ],
    "improdutivo": [
        "feliz natal",
        "parabéns",
        "obrigado",
        "mensagem social",
        "bom dia",
        "boa tarde",
        "felicidades",
        "bom final de semana",
        "apenas informando",
        "sem necessidade de retorno",
        "não precisa fazer nada",
        "tudo resolvido internamente",
        "podem ignorar"
    ]
}

# Criar embeddings de referência só 1 vez (se disponível e em localhost)
if SEMANTIC_AVAILABLE and model is not None:
    ref_embeddings = {
        cat: model.encode(frases)
        for cat, frases in REFERENCIAS.items()
    }
else:
    ref_embeddings = {}


def classify_email_semantic(text: str) -> dict:
    """
    Classificação usando MiniLM com heurísticas inteligentes.
    Faz fallback para NLP se sentence-transformers não estiver disponível.
    """
    if not SEMANTIC_AVAILABLE:
        # Fallback para NLP quando semântico não está disponível
        resultado = classify_email_nlp(text)
        return {
            "categoria": resultado["categoria"],
            "analise_semantica": {
                "similaridade_produtivo": 0,
                "similaridade_improdutivo": 0,
                "diferenca": 0,
                "nota": "Modo semântico não disponível (usando NLP como fallback)"
            },
            "confianca": f"{resultado['confianca']}%"
        }
    
    texto_lower = text.lower()

    # 1) 🔍 Regra de negação — domina tudo
    for n in NEGACOES:
        if n in texto_lower:
            return {
                "categoria": "IMPRODUTIVO",
                "analise_semantica": {
                    "similaridade_produtivo": 0,
                    "similaridade_improdutivo": 100,
                    "diferenca": 100
                },
                "confianca": "AUTO (detecção de negação)"
            }

    # 2) 🔍 Embeddings semânticos normais
    texto_embedding = model.encode([text])[0]

    sim_prod = np.mean(cosine_similarity([texto_embedding], ref_embeddings["produtivo"])[0])
    sim_improd = np.mean(cosine_similarity([texto_embedding], ref_embeddings["improdutivo"])[0])

    # 3) 🔍 Soft decision
    if sim_prod >= sim_improd:
        categoria = "PRODUTIVO"
    else:
        categoria = "IMPRODUTIVO"

    return {
        "categoria": categoria,
        "analise_semantica": {
            "similaridade_produtivo": round(float(sim_prod * 100), 2),
            "similaridade_improdutivo": round(float(sim_improd * 100), 2),
            "diferenca": round(float(abs(sim_prod - sim_improd) * 100), 2)
        },
        "confianca": f"{round(float(abs(sim_prod - sim_improd) * 100), 1)}%"
    }


def generate_reply_semantic(text: str, categoria: str) -> str:
    """
    Resposta template baseada na categoria semântica
    Faz fallback para NLP se sentence-transformers não estiver disponível.
    """
    if not SEMANTIC_AVAILABLE:
        # Fallback para NLP quando semântico não está disponível
        return generate_reply_nlp(text, categoria)
    
    if categoria == "PRODUTIVO":
        return """Olá!

Recebemos sua solicitação e nossa equipe já está analisando.
Retornaremos com uma resposta em breve.

Atenciosamente,
Equipe de Atendimento"""
    else:
        return """Olá!

Muito obrigado pela sua mensagem!
Ficamos felizes com o contato.

Atenciosamente,
Equipe"""
