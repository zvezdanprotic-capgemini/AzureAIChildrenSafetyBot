import time
from typing import List, Dict

_alerts: List[Dict] = []


def trigger_alert(kind: str, session_id: str, detail: dict):
    _alerts.append({
        'timestamp': time.time(),
        'kind': kind,
        'session_id': session_id,
        'detail': detail
    })


def list_alerts(limit: int = 50) -> List[Dict]:
    return _alerts[-limit:]
