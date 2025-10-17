from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional
import time

@dataclass
class Interaction:
    role: str  # 'user' | 'bot'
    content: str
    timestamp: float
    categories: Optional[dict] = None  # content safety categories if available

# In-memory store keyed by session_id
_store: Dict[str, Deque[Interaction]] = defaultdict(lambda: deque(maxlen=100))


def add_interaction(session_id: str, role: str, content: str, categories: dict | None = None):
    _store[session_id].append(Interaction(role=role, content=content, timestamp=time.time(), categories=categories))


def get_recent_interactions(session_id: str, limit: int = 20) -> List[Interaction]:
    if session_id not in _store:
        return []
    dq = _store[session_id]
    return list(dq)[-limit:]


def prune_older_than(seconds: int):
    cutoff = time.time() - seconds
    to_delete = []
    for session_id, dq in _store.items():
        filtered = deque([i for i in dq if i.timestamp >= cutoff], maxlen=100)
        if filtered:
            _store[session_id] = filtered
        else:
            to_delete.append(session_id)
    for sid in to_delete:
        del _store[sid]


def list_sessions() -> List[str]:
    return list(_store.keys())
