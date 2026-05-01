from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend/templates")
)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:7860"]}})


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")
# ---------------- ANALYZE PIPELINE ----------------
@app.route("/analyze", methods=["POST"])
def analyze():

    # -------- FILE INGESTION --------
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        df = pd.read_csv(file)
    except Exception:
        return jsonify({"error": "Invalid file format"}), 400

    log_agent_step("file_ingestion", output_data=f"{len(df)} rows loaded")

    # -------- REPORT UNDERSTANDING --------
    summary = understand_report(df)

    log_agent_step("report_understanding", output_data=summary)

    # -------- ANOMALY DETECTION --------
    anomalies = detect_anomalies(summary)

    log_agent_step("anomaly_detection", output_data=anomalies)

    # -------- INTENT CLASSIFICATION --------
    query = "analyze sustainability and financial risks"

    intent = classify_intent(query)

    log_agent_step("intent_classifier", input_data=query, output_data=intent)

    # -------- RAG INDEX --------
    context_text = str(summary)

    embed_texts(context_text, tag=intent)

    # -------- CONTEXT RETRIEVAL --------
    context = retrieve_context(query)

    log_agent_step("rag_retrieval", output_data=context)

    # -------- ROOT CAUSE --------
    root_cause = explain_root_cause(query, context, intent)

    log_agent_step("root_cause_reasoning", output_data=root_cause)

    # -------- COUNTERFACTUAL SIMULATION --------
    counterfactual = simulate_counterfactual(
    intent,
    root_cause,
    anomalies
)

    log_agent_step("counterfactual_simulation", output_data=counterfactual)

    # -------- RECOMMENDATIONS --------
    recommendations = recommend_actions(
    root_cause,
    anomalies
)

    log_agent_step("action_recommendation", output_data=recommendations)

    # -------- DECISION CONFIDENCE --------
# -------- DECISION CONFIDENCE --------
    confidence = assess_decision_confidence(
    intent,
    root_cause,
    anomalies,
    counterfactual
)
    log_agent_step("decision_confidence", output_data=confidence)

    # -------- SCORE CALCULATION --------
    sustainability_score = max(50, 85 - len(anomalies) * 5)

    # -------- FINAL RESPONSE --------
    response = {
        "sustainability_score": sustainability_score,
        "root_cause": root_cause,
        "anomalies": anomalies,
        "recommendations": recommendations,
        "confidence": confidence
    }

    return jsonify(response)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "7860")), debug=False)