"""
Counterfactual Simulation Agent
--------------------------------
Simulates "what-if" sustainability and financial risk scenarios
for the SustainAI platform.
"""

from datetime import datetime
from typing import List, Optional, Dict


def simulate_counterfactual(
    intent: str,
    root_cause: str,
    anomalies: Optional[List[dict]] = None
) -> Dict:

    rc = (root_cause or "").lower()
    intent = (intent or "").upper()
    anomalies = anomalies or []

    # ---------------------------------
    # CARBON EXPOSURE SCENARIO
    # ---------------------------------
    if "carbon" in rc or "emission" in rc or "energy" in rc:
        return {
            "scenario": "Reduce exposure to high-carbon sectors by 20%",
            "impact": "Estimated +9 point improvement in sustainability score and 28% reduction in climate transition risk",
            "risk": "Short-term portfolio volatility due to sector rebalancing",
            "confidence": "High",
            "category": "Climate Risk Simulation",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # ESG IMPROVEMENT SCENARIO
    # ---------------------------------
    if "esg" in rc or "sustainability" in rc:
        return {
            "scenario": "Increase ESG-compliant asset allocation by 15%",
            "impact": "Projected ESG score increase from 74 → 86 and improved sustainability ranking",
            "risk": "Requires portfolio restructuring and additional ESG data monitoring",
            "confidence": "High",
            "category": "Sustainability Optimization",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # GREEN BOND INVESTMENT SCENARIO
    # ---------------------------------
    if "green bond" in rc or "sustainable investment" in rc:
        return {
            "scenario": "Increase green bond allocation from 12% to 20%",
            "impact": "Improved sustainability rating and projected +1.5% long-term portfolio stability",
            "risk": "Market liquidity constraints in emerging green bond markets",
            "confidence": "Medium-High",
            "category": "Sustainable Finance Strategy",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # FINANCIAL OPERATIONAL SCENARIO
    # ---------------------------------
    if "decline" in rc or "authorization" in rc:
        return {
            "scenario": "Adjust transaction authorization thresholds by 1.5%",
            "impact": "+1.4% improvement in transaction approval rates",
            "risk": "Potential increase in fraud exposure if thresholds are relaxed excessively",
            "confidence": "Medium",
            "category": "Financial Operations",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # SETTLEMENT EFFICIENCY SCENARIO
    # ---------------------------------
    if "settlement" in rc or "delay" in rc:
        return {
            "scenario": "Optimize settlement batching and regional clearing times",
            "impact": "-30% average settlement delay and improved liquidity flow",
            "risk": "Operational coordination required across multiple clearing partners",
            "confidence": "Medium",
            "category": "Operational Efficiency",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # ANOMALY-DRIVEN SCENARIO
    # ---------------------------------
    if anomalies and len(anomalies) >= 3:
        return {
            "scenario": "Deploy real-time AI anomaly monitoring across financial streams",
            "impact": "Early detection of financial and sustainability risks, reducing incident response time by 40%",
            "risk": "Requires additional compute resources for continuous monitoring",
            "confidence": "Medium",
            "category": "Risk Monitoring",
            "generated_at": datetime.utcnow().isoformat()
        }

    # ---------------------------------
    # FALLBACK
    # ---------------------------------
    return {
        "scenario": "Current financial and sustainability configuration appears stable",
        "impact": "No significant improvement predicted beyond ±1% change in sustainability score",
        "risk": "Low operational risk detected",
        "confidence": "Low",
        "category": "Baseline Analysis",
        "generated_at": datetime.utcnow().isoformat()
    }