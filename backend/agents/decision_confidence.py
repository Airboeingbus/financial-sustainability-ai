"""
Decision Confidence Guardrail Agent
-----------------------------------
Evaluates confidence and governance risk for SustainAI decisions.

Purpose:
• Prevent overconfident automation
• Signal when human ESG risk review is needed
• Provide explainable AI decision confidence
"""

from typing import Dict, List, Optional
from datetime import datetime


def assess_decision_confidence(
    intent: str,
    root_cause: str,
    anomalies: Optional[List[dict]] = None,
    counterfactual: Optional[Dict] = None,
    historical_accuracy: Optional[float] = None
) -> Dict:

    anomalies = anomalies or []
    score = 0.0
    reasons = []
    risk_flags = []

    intent = (intent or "").upper()
    rc_lower = (root_cause or "").lower()

    # ------------------------------------------------
    # 1. Intent Confidence (0 - 0.30)
    # ------------------------------------------------

    INTENT_CONFIDENCE = {
        "ESG_ANALYSIS": 0.30,
        "SUSTAINABILITY_SCORE": 0.30,
        "RISK_ANALYSIS": 0.28,
        "PERFORMANCE_REPORT": 0.25,
        "PORTFOLIO_OPTIMIZATION": 0.22,
        "ANOMALY_DETECTION": 0.27
    }

    intent_score = INTENT_CONFIDENCE.get(intent, 0.15)
    score += intent_score

    if intent_score >= 0.28:
        reasons.append(f"High-confidence intent classification: {intent}")
    elif intent_score >= 0.20:
        reasons.append(f"Moderate-confidence intent classification: {intent}")
    else:
        reasons.append(f"Low-confidence intent classification: {intent}")
        risk_flags.append("Uncertain intent classification")

    # ------------------------------------------------
    # 2. Anomaly Evidence Strength (0 - 0.25)
    # ------------------------------------------------

    if len(anomalies) >= 3:
        score += 0.25
        reasons.append(f"Strong anomaly evidence ({len(anomalies)} signals detected)")
    elif len(anomalies) >= 1:
        score += 0.18
        reasons.append(f"Moderate anomaly evidence ({len(anomalies)} signals)")
    else:
        score += 0.08
        reasons.append("Limited anomaly evidence")
        risk_flags.append("Weak anomaly signal")

    # detect high severity anomalies
    high_severity_count = sum(
        1 for a in anomalies if str(a.get("severity", "")).lower() in ["high", "critical"]
    )

    if high_severity_count > 0:
        score += 0.05
        reasons.append(f"High-severity anomalies detected ({high_severity_count})")

    # ------------------------------------------------
    # 3. Root Cause Quality (0 - 0.20)
    # ------------------------------------------------

    rc_length = len(root_cause or "")

    sustainability_keywords = [
        "carbon",
        "emission",
        "climate",
        "esg",
        "sustainability",
        "energy",
        "portfolio",
        "risk"
    ]

    keyword_matches = sum(1 for k in sustainability_keywords if k in rc_lower)

    if rc_length > 200 and keyword_matches >= 3:
        score += 0.20
        reasons.append("Detailed sustainability risk reasoning detected")
    elif rc_length > 100:
        score += 0.15
        reasons.append("Moderate causal explanation depth")
    else:
        score += 0.08
        reasons.append("Limited causal reasoning depth")
        risk_flags.append("Shallow root cause explanation")

    # ------------------------------------------------
    # 4. Counterfactual Validation (0 - 0.15)
    # ------------------------------------------------

    if counterfactual:

        cf_confidence = counterfactual.get("confidence", "Low")

        if cf_confidence in ["High", "Medium-High"]:
            score += 0.15
            reasons.append("Strong counterfactual validation")
        elif cf_confidence == "Medium":
            score += 0.12
            reasons.append("Moderate counterfactual support")
        else:
            score += 0.08
            reasons.append("Weak counterfactual validation")
            risk_flags.append("Low simulation confidence")

    else:
        score += 0.05
        reasons.append("No counterfactual validation available")
        risk_flags.append("Missing scenario analysis")

    # ------------------------------------------------
    # 5. Historical Model Accuracy (0 - 0.10)
    # ------------------------------------------------

    if historical_accuracy is not None:

        if historical_accuracy >= 0.85:
            score += 0.10
            reasons.append(f"Strong historical accuracy ({historical_accuracy:.1%})")
        elif historical_accuracy >= 0.70:
            score += 0.07
            reasons.append(f"Moderate historical accuracy ({historical_accuracy:.1%})")
        else:
            score += 0.03
            reasons.append(f"Low historical accuracy ({historical_accuracy:.1%})")
            risk_flags.append("Weak historical performance")

    # ------------------------------------------------
    # Normalize score
    # ------------------------------------------------

    score = min(score, 1.0)

    # ------------------------------------------------
    # Decision Classification
    # ------------------------------------------------

    if score >= 0.80:
        level = "HIGH"
        escalation = False
        recommendation = "Suitable for automated execution with monitoring"

    elif score >= 0.65:
        level = "MEDIUM-HIGH"
        escalation = False
        recommendation = "Proceed with enhanced monitoring"

    elif score >= 0.50:
        level = "MEDIUM"
        escalation = True
        recommendation = "Human review recommended"

    elif score >= 0.35:
        level = "MEDIUM-LOW"
        escalation = True
        recommendation = "Human approval required"

    else:
        level = "LOW"
        escalation = True
        recommendation = "Manual investigation required"

    # ------------------------------------------------
    # Risk Level
    # ------------------------------------------------

    if len(risk_flags) >= 3:
        risk_level = "HIGH"
    elif len(risk_flags) >= 2:
        risk_level = "MEDIUM"
    elif len(risk_flags) >= 1:
        risk_level = "LOW"
    else:
        risk_level = "MINIMAL"

    return {
        "confidence_score": round(score, 3),
        "confidence_level": level,
        "human_review_required": escalation,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "risk_flags": risk_flags,
        "rationale": reasons,
        "decision_metadata": {
            "intent": intent,
            "anomaly_count": len(anomalies),
            "high_severity_anomalies": high_severity_count,
            "counterfactual_available": counterfactual is not None,
            "assessed_at": datetime.utcnow().isoformat()
        }
    }