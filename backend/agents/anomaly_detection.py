# anomaly_detection_agent.py

def detect_anomalies(summary: dict):
    """
    Detect operational, financial, and sustainability anomalies
    from aggregated financial metrics.
    """

    anomalies = []
    key_metrics = summary.get("key_metrics", {})

    # --- Authorization decline spike ---
    if "decline_rate" in key_metrics:
        mean_decline = key_metrics["decline_rate"].get("mean", 0)

        if mean_decline > 15:
            anomalies.append({
                "type": "AUTH_DECLINE_SPIKE",
                "severity": "high",
                "metric": "declined_txns",
                "category": "Financial Risk",
                "message": f"High authorization decline rate detected (avg {mean_decline:.1f})"
            })

    # --- Settlement delays ---
    if "delay_hours" in key_metrics:
        mean_delay = key_metrics["delay_hours"].get("mean", 0)

        if mean_delay > 2:
            anomalies.append({
                "type": "SETTLEMENT_DELAY",
                "severity": "medium",
                "metric": "delay_hours",
                "category": "Operational Risk",
                "message": f"Settlement delays unusually high (avg {mean_delay:.1f} hrs)"
            })

    # --- Carbon exposure anomaly ---
    if "carbon_intensity" in key_metrics:
        carbon_score = key_metrics["carbon_intensity"].get("mean", 0)

        if carbon_score > 70:
            anomalies.append({
                "type": "HIGH_CARBON_EXPOSURE",
                "severity": "high",
                "metric": "carbon_intensity",
                "category": "Climate Risk",
                "message": f"High carbon exposure detected (score {carbon_score:.1f})"
            })

    # --- ESG score drop ---
    if "esg_score" in key_metrics:
        esg_score = key_metrics["esg_score"].get("mean", 0)

        if esg_score < 50:
            anomalies.append({
                "type": "LOW_ESG_SCORE",
                "severity": "medium",
                "metric": "esg_score",
                "category": "Sustainability Risk",
                "message": f"ESG sustainability score is below recommended threshold ({esg_score:.1f})"
            })

    # --- Unusual transaction volume ---
    if "txn_volume" in key_metrics:
        volume = key_metrics["txn_volume"].get("mean", 0)

        if volume > 100000:
            anomalies.append({
                "type": "VOLUME_SPIKE",
                "severity": "medium",
                "metric": "txn_volume",
                "category": "Operational Monitoring",
                "message": f"Unusual spike in transaction volume detected ({volume:.0f})"
            })

    # --- fallback ---
    if not anomalies:
        anomalies.append({
            "type": "NO_ANOMALY",
            "severity": "low",
            "category": "System Status",
            "message": "No significant financial or sustainability anomalies detected"
        })

    return anomalies