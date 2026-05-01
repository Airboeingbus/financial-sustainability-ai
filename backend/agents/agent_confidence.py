"""
Decision Confidence Agent
-------------------------
Evaluates how confident the system is about the final recommendation.
"""

def compute_confidence(anomalies, recommendations):

    anomaly_factor = max(0, 1 - (len(anomalies) * 0.1))
    recommendation_factor = min(1, len(recommendations) * 0.2)

    score = (anomaly_factor + recommendation_factor) / 2

    if score > 0.75:
        level = "High"
    elif score > 0.5:
        level = "Medium"
    else:
        level = "Low"

    return {
        "confidence_score": round(score, 2),
        "confidence_level": level,
        "explanation": "Confidence derived from anomaly severity and recommendation coverage."
    }