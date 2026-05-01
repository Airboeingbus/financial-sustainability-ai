# intent_classifier_agent.py

def classify_intent(query: str) -> str:
    """
    Classify user query intent for SustainAI platform.

    Returns:
        str: Intent category
    """

    if not query:
        return "GENERAL"

    q = query.lower()

    # ---------------------------
    # Sustainability / ESG intents
    # ---------------------------

    if "esg" in q or "sustainability" in q:
        return "ESG_ANALYSIS"

    if "sustainability score" in q or "esg score" in q:
        return "SUSTAINABILITY_SCORE"

    if "carbon" in q or "emission" in q or "climate" in q:
        return "CLIMATE_RISK"

    # ---------------------------
    # Financial / portfolio intents
    # ---------------------------

    if "portfolio" in q or "investment" in q:
        return "PORTFOLIO_ANALYSIS"

    if "risk" in q:
        return "RISK_ANALYSIS"

    if "anomaly" in q or "unusual" in q:
        return "ANOMALY_DETECTION"

    if "recommend" in q or "optimiz" in q or "action" in q:
        return "OPTIMIZATION_RECOMMENDATION"

    # ---------------------------
    # Operational / performance
    # ---------------------------

    if "performance" in q or "network" in q:
        return "PERFORMANCE_REPORT"

    if "authorization" in q or "auth" in q:
        return "AUTH_TRENDS"

    if "settlement" in q or "clearing" in q:
        return "SETTLEMENT_ANALYSIS"

    # ---------------------------
    # fallback
    # ---------------------------

    return "GENERAL"