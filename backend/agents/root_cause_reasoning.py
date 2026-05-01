import os
from openai import OpenAI


def explain_root_cause(query, context, intent):
    """
    Intent-aware AI reasoning for SustainAI financial
    and sustainability risk intelligence.

    Uses LLM when available, otherwise deterministic fallback.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    # -----------------------------
    # SAFE FALLBACK IF NO API KEY
    # -----------------------------
    if not api_key:
        return fallback_reasoning(intent, context)

    try:

        client = OpenAI(api_key=api_key)

        prompt = f"""
You are an AI sustainability and financial risk intelligence analyst.

User Query:
{query}

Intent:
{intent}

Context from uploaded financial reports:
{context}

Instructions:
- Identify the most likely root cause behind the detected anomaly or pattern.
- Consider financial metrics, operational signals, and sustainability indicators.
- Provide concise reasoning suitable for executive dashboards.

Intent guidance:

ESG_ANALYSIS → sustainability risks, ESG score drivers  
CLIMATE_RISK → carbon exposure, emission risk, energy sector concentration  
ANOMALY_DETECTION → unusual transaction patterns or abnormal metrics  
PERFORMANCE_REPORT → overall financial system health  
OPTIMIZATION_RECOMMENDATION → operational or sustainability improvements

Respond in clear business language.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    except Exception:

        # absolute demo safety
        return fallback_reasoning(intent, context)


# ----------------------------------------------------
# FALLBACK REASONING
# ----------------------------------------------------

def fallback_reasoning(intent, context):

    c = str(context).lower()

    # -----------------------------
    # ESG / Sustainability
    # -----------------------------
    if intent == "ESG_ANALYSIS":

        if "esg" in c and "low" in c:
            return (
                "The ESG score decline appears linked to increased exposure "
                "to lower-rated sectors or insufficient sustainability reporting."
            )

        return (
            "Current ESG metrics indicate moderate sustainability exposure "
            "with potential risk arising from sector concentration."
        )

    # -----------------------------
    # Climate risk
    # -----------------------------
    if intent == "CLIMATE_RISK":

        if "carbon" in c or "emission" in c:
            return (
                "Elevated carbon intensity suggests significant exposure to "
                "high-emission sectors, increasing climate transition risk."
            )

        return (
            "Climate exposure appears stable with no immediate emission-driven risks."
        )

    # -----------------------------
    # Financial anomaly
    # -----------------------------
    if intent == "ANOMALY_DETECTION":

        if "decline" in c:
            return (
                "The anomaly is likely driven by elevated transaction decline rates, "
                "potentially linked to stricter authorization rules or risk controls."
            )

        if "delay" in c:
            return (
                "Operational settlement delays indicate bottlenecks in processing "
                "pipelines or clearing schedules."
            )

        return (
            "Transaction patterns show minor anomalies that may arise from "
            "temporary operational fluctuations."
        )

    # -----------------------------
    # Performance analysis
    # -----------------------------
    if intent == "PERFORMANCE_REPORT":

        return (
            "Financial system performance appears influenced by transaction "
            "processing efficiency and anomaly signals across the dataset."
        )

    # -----------------------------
    # Optimization recommendation
    # -----------------------------
    if intent == "OPTIMIZATION_RECOMMENDATION":

        return (
            "Improving portfolio sustainability exposure and refining "
            "risk monitoring thresholds could stabilize financial and ESG metrics."
        )

    # -----------------------------
    # general fallback
    # -----------------------------
    return (
        "Observed financial and sustainability signals suggest moderate "
        "operational and ESG-related risk factors influencing system behavior."
    )