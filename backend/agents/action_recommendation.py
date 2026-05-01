# action_recommendation_agent.py

def recommend_actions(explanation: str, anomalies: list | None = None):
    """
    Generate operational and sustainability-focused recommendations
    based on root cause explanation and detected anomalies.
    """

    actions = []
    text = explanation.lower() if explanation else ""

    # --- Financial transaction risk ---
    if "decline" in text or "authorization" in text:
        actions.append({
            "title": "Optimize Authorization Logic",
            "action": "Review authorization rules, retry logic, and fraud filters.",
            "impact": "Improves approval rates and transaction throughput.",
            "priority": "High",
            "owner": "Authorization Operations",
            "confidence": 0.86,
            "category": "Financial Risk"
        })

    # --- Settlement risk ---
    if "settlement" in text or "delay" in text:
        actions.append({
            "title": "Improve Settlement Efficiency",
            "action": "Optimize settlement batching and regional clearing schedules.",
            "impact": "Reduces settlement delays and improves liquidity flow.",
            "priority": "Medium",
            "owner": "Settlement Operations",
            "confidence": 0.78,
            "category": "Operational Risk"
        })

    # --- Carbon exposure / climate risk ---
    if "carbon" in text or "emission" in text or "energy" in text:
        actions.append({
            "title": "Reduce Carbon Exposure",
            "action": "Rebalance portfolio toward low-carbon or renewable sectors.",
            "impact": "Reduces climate transition risk and improves ESG sustainability score.",
            "priority": "High",
            "owner": "Sustainability Risk Team",
            "confidence": 0.83,
            "category": "Climate Risk"
        })

    # --- ESG risk ---
    if "esg" in text or "sustainability" in text:
        actions.append({
            "title": "Enhance ESG Compliance Monitoring",
            "action": "Integrate ESG data sources and improve sustainability reporting.",
            "impact": "Strengthens ESG transparency and improves sustainability risk scoring.",
            "priority": "Medium",
            "owner": "ESG Compliance Team",
            "confidence": 0.76,
            "category": "Sustainability"
        })

    # --- Green finance opportunity ---
    if "green bond" in text or "sustainable investment" in text:
        actions.append({
            "title": "Increase Green Investment Allocation",
            "action": "Expand allocation toward green bonds and sustainable financial instruments.",
            "impact": "Improves sustainability performance and aligns with ESG investment strategies.",
            "priority": "Medium",
            "owner": "Portfolio Management",
            "confidence": 0.74,
            "category": "Sustainable Finance"
        })

    # --- Use anomaly signals ---
    if anomalies:
        high_severity = [
            a for a in anomalies
            if str(a.get("severity", "")).lower() in ["high", "critical"]
        ]

        if len(high_severity) >= 3:
            actions.append({
                "title": "Deploy Real-Time Risk Monitoring",
                "action": "Implement AI-driven monitoring for transaction anomalies.",
                "impact": "Enables early detection of financial and sustainability risks.",
                "priority": "High",
                "owner": "Risk Intelligence Team",
                "confidence": 0.80,
                "category": "Risk Monitoring"
            })

    # --- fallback action ---
    if not actions:
        actions.append({
            "title": "Continue Monitoring",
            "action": "No critical issues detected. Maintain continuous monitoring of transaction and ESG metrics.",
            "impact": "Ensures system stability and sustainability compliance.",
            "priority": "Low",
            "owner": "Network Monitoring",
            "confidence": 0.60,
            "category": "Monitoring"
        })

    return actions