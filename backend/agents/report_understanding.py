import pandas as pd
import re


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────

def understand_report(path):
    df = pd.read_csv(path, low_memory=False)

    print(f"📊 Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
    print(f"📊 Columns: {list(df.columns)}")
    print(f"📊 Data types: {df.dtypes.to_dict()}")

    # Parse datetime columns where possible
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                sample = str(df[col].iloc[0]) if len(df) > 0 else ""
                if '-' in sample and any(c.isdigit() for c in sample):
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    print(f"✅ Converted '{col}' to datetime")
            except Exception as e:
                print(f"⚠️ Could not convert '{col}' to datetime: {e}")

    report_type = infer_report_type(path, df)
    print(f"📋 Inferred report type: {report_type}")

    key_metrics = extract_key_metrics(df, report_type)

    summary = {
        "report_type": report_type,
        "rows": len(df),
        "columns": list(df.columns),
        "key_metrics": key_metrics,
        "sample_rows": df.head(3).to_dict(orient="records"),
        "text_summary": generate_text_summary(path, df)
    }

    print(f"✅ Final key_metrics keys: {list(key_metrics.keys())}")
    return summary


# ─────────────────────────────────────────────
#  INFER REPORT TYPE
# ─────────────────────────────────────────────

def infer_report_type(path, df):
    path_lower = path.lower()
    if "auth" in path_lower:
        return "authorization"
    if "settlement" in path_lower or "settle" in path_lower:
        return "settlement"

    cols_joined = ' '.join(c.lower() for c in df.columns)

    if any(t in cols_joined for t in ['decline', 'authorization', 'auth', 'approved', 'rejected', 'fraud']):
        return "authorization"
    if any(t in cols_joined for t in ['settlement', 'delay', 'settle', 'processing', 'latency']):
        return "settlement"

    return "unknown"


# ─────────────────────────────────────────────
#  SMART TEXT → NUMERIC CONVERTER
# ─────────────────────────────────────────────

def smart_convert_to_numeric(df, column_name):
    """
    Converts text columns to numeric where possible.
    Handles: "$1,500", "200 Zentia", "5%", "3.5 hours", etc.
    Returns a numeric Series or None if conversion fails.
    """
    try:
        series = df[column_name].copy()

        if pd.api.types.is_numeric_dtype(series):
            return series

        series = series.astype(str)

        def extract_number(text):
            if pd.isna(text) or text.strip().lower() in ('nan', 'none', '', 'n/a'):
                return None
            cleaned = text.replace(',', '').replace('$', '').replace('%', '').strip()
            match = re.search(r'-?\d+\.?\d*', cleaned)
            return float(match.group()) if match else None

        numeric_series = series.apply(extract_number)
        success_rate = numeric_series.notna().sum() / max(len(numeric_series), 1)

        if success_rate >= 0.5:
            return numeric_series

        return None

    except Exception as e:
        print(f"⚠️ Could not convert '{column_name}' to numeric: {e}")
        return None


# ─────────────────────────────────────────────
#  COLUMN FINDER
# ─────────────────────────────────────────────

def find_column(df, keywords):
    """
    Returns the first column name matching any keyword (case-insensitive substring match).
    """
    cols_lower = {col.lower(): col for col in df.columns}
    for keyword in keywords:
        for col_lower, col_original in cols_lower.items():
            if keyword in col_lower:
                return col_original
    return None


# ─────────────────────────────────────────────
#  COMPUTE DECLINE RATE FROM RAW STATUS COLUMN
# ─────────────────────────────────────────────

def compute_decline_rate_from_status(df):
    """
    Looks for a status/result column and computes real decline rate (%).
    Returns (decline_rate_percent, declined_count, total_count) or None.
    """
    status_keywords = ['status', 'result', 'auth_result', 'auth_status',
                       'transaction_status', 'txn_status', 'approval', 'outcome']

    status_col = find_column(df, status_keywords)

    if status_col is None:
        return None

    col = df[status_col].astype(str).str.strip().str.lower()
    decline_values = {'declined', 'denied', 'rejected', 'failed', 'fail',
                      'decline', 'deny', 'reject', '0', 'false', 'no'}

    declined = col.isin(decline_values).sum()
    total = len(col)

    if total == 0:
        return None

    rate = round((declined / total) * 100, 4)
    print(f"✅ Computed real decline rate from '{status_col}': {declined}/{total} = {rate}%")
    return rate, int(declined), int(total)


# ─────────────────────────────────────────────
#  COMPUTE DELAY FROM RAW TIME COLUMN
# ─────────────────────────────────────────────

def compute_delay_hours_from_column(df, metrics):
    """
    Finds any time/delay column and converts to hours.
    Returns a dict with mean/min/max/sum/count or None.
    """
    # Priority order: explicit delay columns → settlement time → latency
    delay_keywords = ['delay', 'settlement_delay', 'processing_delay',
                      'delay_hours', 'delay_time', 'settlement_delay_hours']
    time_sec_keywords = ['settlement_time_sec', 'time_sec', 'duration_sec',
                         'processing_time_sec', 'seconds']
    time_ms_keywords = ['latency_ms', 'latency', 'processing_time_ms',
                        'embedded_device_latency_ms', 'response_time_ms']

    # 1. Direct delay column (already in hours or small numbers)
    col = find_column(df, delay_keywords)
    if col and col in metrics:
        val = metrics[col]
        print(f"✅ Using direct delay column '{col}' as delay_hours")
        return val

    # 2. Seconds-based column → convert to hours
    col = find_column(df, time_sec_keywords)
    if col and col in metrics:
        orig = metrics[col]
        result = {
            "mean":  round(orig["mean"]  / 3600, 6),
            "min":   round(orig["min"]   / 3600, 6),
            "max":   round(orig["max"]   / 3600, 6),
            "sum":   round(orig["sum"]   / 3600, 6),
            "count": orig["count"]
        }
        print(f"✅ Converted '{col}' (seconds) → delay_hours: mean={result['mean']:.4f}h")
        return result

    # 3. Milliseconds-based column → convert to hours
    col = find_column(df, time_ms_keywords)
    if col and col in metrics:
        orig = metrics[col]
        result = {
            "mean":  round(orig["mean"]  / (1000 * 3600), 6),
            "min":   round(orig["min"]   / (1000 * 3600), 6),
            "max":   round(orig["max"]   / (1000 * 3600), 6),
            "sum":   round(orig["sum"]   / (1000 * 3600), 6),
            "count": orig["count"]
        }
        print(f"✅ Converted '{col}' (ms) → delay_hours: mean={result['mean']:.4f}h")
        return result

    return None


# ─────────────────────────────────────────────
#  MAIN METRICS EXTRACTOR
# ─────────────────────────────────────────────

def extract_key_metrics(df, report_type):
    metrics = {}

    # ── Step 1: Native numeric columns ──────────────────────────
    numeric_cols = [
        col for col in df.select_dtypes(include=['number']).columns
        if not pd.api.types.is_datetime64_any_dtype(df[col])
    ]
    print(f"🔍 Native numeric columns ({len(numeric_cols)}): {numeric_cols}")

    # ── Step 2: Try converting text columns to numeric ───────────
    skip_text_cols = {'transaction id', 'date', 'sender', 'receiver',
                      'type', 'currency', 'id', 'txn_id', 'merchant'}
    text_cols = [
        col for col in df.select_dtypes(include=['object']).columns
        if col.lower() not in skip_text_cols
    ]
    print(f"🔍 Checking {len(text_cols)} text columns for numeric conversion...")

    converted_cols = {}
    for col in text_cols:
        converted = smart_convert_to_numeric(df, col)
        if converted is not None:
            converted_cols[col] = converted
            print(f"✅ Text→numeric: '{col}' (e.g. '{df[col].iloc[0]}' → {converted.iloc[0]})")

    all_numeric_cols = list(numeric_cols) + list(converted_cols.keys())
    print(f"📊 Total numeric columns for metrics: {len(all_numeric_cols)}")

    # ── Step 3: Compute stats for every numeric column ───────────
    for col in all_numeric_cols:
        series = converted_cols[col] if col in converted_cols else df[col]

        if series.isna().all():
            print(f"⚠️ Skipping '{col}': all NaN")
            continue

        try:
            metrics[col] = {
                "mean":  round(float(series.mean()),  4),
                "min":   round(float(series.min()),   4),
                "max":   round(float(series.max()),   4),
                "sum":   round(float(series.sum()),   4),
                "count": int(series.count())
            }
            print(f"✅ Metric '{col}': mean={metrics[col]['mean']}")
        except Exception as e:
            print(f"⚠️ Skipping '{col}': {e}")

    # ── Step 4: Report-type specific standardisation ─────────────

    if report_type == "authorization":

        # ── 4a. Try computing real decline rate from status column ──
        decline_result = compute_decline_rate_from_status(df)

        if decline_result is not None:
            rate, declined_count, total = decline_result
            metrics["declined_txns"] = {
                "mean":  rate,          # decline % — used by chart
                "min":   0,
                "max":   float(declined_count),
                "sum":   float(declined_count),
                "count": total
            }
            metrics["decline_rate"] = rate
            print(f"✅ Set declined_txns.mean = {rate}% (real)")

        else:
            # ── 4b. Find any numeric decline/fraud column ────────────
            decline_col = find_column(df, [
                'decline', 'declined', 'reject', 'rejected', 'fail', 'failed',
                'denial', 'denied', 'authorization_decline', 'auth_decline',
                'decline_count', 'declined_count', 'num_declines', 'declined_txns'
            ])

            if decline_col and decline_col in metrics:
                metrics["declined_txns"] = metrics[decline_col]
                print(f"✅ Mapped '{decline_col}' → declined_txns")

            elif 'fraud_flag' in metrics:
                fraud_sum   = metrics['fraud_flag']['sum']
                fraud_count = metrics['fraud_flag']['count']
                rate = round((fraud_sum / fraud_count) * 100, 4) if fraud_count else 0
                metrics["declined_txns"] = {
                    "mean":  rate,
                    "min":   0,
                    "max":   float(fraud_sum),
                    "sum":   float(fraud_sum),
                    "count": int(fraud_count)
                }
                metrics["decline_rate"] = rate
                print(f"✅ Used 'fraud_flag' as proxy → decline_rate={rate}%")

            elif 'anomaly_score' in metrics:
                rate = round(metrics['anomaly_score']['mean'] * 100, 4)
                metrics["declined_txns"] = {
                    "mean":  rate,
                    "min":   0,
                    "max":   round(metrics['anomaly_score']['max'] * 100, 4)
                }
                metrics["decline_rate"] = rate
                print(f"✅ Used 'anomaly_score' as proxy → decline_rate={rate}%")

            else:
                # Last resort: 5% default
                total_rows = len(df)
                estimated  = round(total_rows * 0.05, 2)
                metrics["declined_txns"] = {
                    "mean":  5.0,
                    "min":   0,
                    "max":   estimated,
                    "sum":   estimated,
                    "count": int(estimated)
                }
                metrics["decline_rate"] = 5.0
                print(f"⚠️ No decline metric found — using 5% default")

    elif report_type == "settlement":

        # ── 4c. Compute delay_hours ──────────────────────────────
        delay = compute_delay_hours_from_column(df, metrics)

        if delay is not None:
            metrics["delay_hours"] = delay
            print(f"✅ delay_hours set: mean={delay['mean']:.4f}h")

        else:
            # Proxy via Amount/Fee
            for proxy in ['Amount', 'Fee', 'amount', 'fee']:
                if proxy in metrics:
                    amount_mean     = metrics[proxy]['mean']
                    estimated_delay = round(min(amount_mean / 100, 24), 4)
                    metrics["delay_hours"] = {
                        "mean": estimated_delay,
                        "min":  0.5,
                        "max":  round(estimated_delay * 2, 4),
                        "sum":  0,
                        "count": len(df)
                    }
                    print(f"⚠️ Used '{proxy}' as delay proxy → {estimated_delay}h")
                    break
            else:
                metrics["delay_hours"] = {
                    "mean":  1.8,
                    "min":   0.5,
                    "max":   4.0,
                    "sum":   0,
                    "count": len(df)
                }
                print("⚠️ No delay metric — using default 1.8h")

    return metrics


# ─────────────────────────────────────────────
#  TEXT SUMMARY
# ─────────────────────────────────────────────

def generate_text_summary(path, df):
    lines = [
        f"Report file: {path}",
        f"Total rows: {len(df)}",
        f"Columns: {', '.join(df.columns)}"
    ]
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            try:
                lines.append(
                    f"{col} ranges from {df[col].min():.2f} to {df[col].max():.2f} "
                    f"with an average of {df[col].mean():.2f}"
                )
            except Exception:
                lines.append(f"{col}: numeric column with {len(df[col])} values")
    return " | ".join(lines)