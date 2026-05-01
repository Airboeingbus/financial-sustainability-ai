# agent_logger.py

import time
from datetime import datetime
import uuid

# In-memory agent execution log (demo-safe)
_AGENT_LOGS = []


def log_agent_step(
    agent_name: str,
    input_data=None,
    output_data=None,
    metadata: dict = None,
    status: str = "success",
    level: str = "info",
    request_id: str = None,
    start_time: float = None
):
    """
    Log a single agent execution step.

    Args:
        agent_name (str): Name of the agent
        input_data (any): Input given to the agent
        output_data (any): Output produced by the agent
        metadata (dict): Optional metadata (severity, intent, etc.)
        status (str): success | error | warning
        level (str): info | debug | warning | error
        request_id (str): ID for tracking a pipeline request
        start_time (float): optional start time for execution tracking
    """

    end_time = time.time()

    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_name,
        "status": status,
        "level": level,
        "request_id": request_id,
        "execution_time_ms": (
            round((end_time - start_time) * 1000, 2) if start_time else None
        ),
        "input": _safe_stringify(input_data),
        "output": _safe_stringify(output_data),
        "metadata": metadata or {}
    }

    _AGENT_LOGS.append(log_entry)


def get_agent_logs(limit: int = 50):
    """
    Retrieve recent agent logs (most recent last).
    """
    return _AGENT_LOGS[-limit:]


def get_logs_by_request(request_id: str):
    """
    Retrieve logs belonging to a specific pipeline execution.
    """
    return [log for log in _AGENT_LOGS if log.get("request_id") == request_id]


def clear_agent_logs():
    """
    Clear all logs (useful between demos).
    """
    _AGENT_LOGS.clear()


# -------------------- HELPERS --------------------

def _safe_stringify(obj):
    """
    Convert objects to readable strings without crashing.
    """

    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    try:
        return str(obj)
    except Exception:
        return "<unserializable>"