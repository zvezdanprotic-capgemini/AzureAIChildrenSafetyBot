from typing import Dict, Any, List
from interaction_store import get_recent_interactions

# Simple heuristic risk scoring.
# Factors: repeated blocked attempts, increasing severity categories, presence of self-harm or sexual queries.

def assess_risk(session_id: str) -> Dict[str, Any]:
    interactions = get_recent_interactions(session_id, limit=30)
    risk_score = 0
    flags: List[str] = []

    # Count user messages containing certain patterns (very naive placeholder)
    boundary_terms = ["bypass", "ignore rules", "jailbreak", "how to harm", "suicide"]
    boundary_hits = 0
    sexual_hits = 0
    self_harm_hits = 0

    for inter in interactions:
        if inter.role != 'user':
            continue
        lower = inter.content.lower()
        if any(term in lower for term in boundary_terms):
            boundary_hits += 1
        if inter.categories:
            if inter.categories.get('sexual', 0) >= 1:
                sexual_hits += 1
            if inter.categories.get('self_harm', 0) >= 1:
                self_harm_hits += 1

    risk_score += boundary_hits * 2 + sexual_hits * 3 + self_harm_hits * 5

    if boundary_hits >= 2:
        flags.append('repeated_boundary_probing')
    if self_harm_hits >= 1:
        flags.append('self_harm_interest')
    if sexual_hits >= 2:
        flags.append('repeated_sexual_topic')

    # Normalize simple risk levels
    if risk_score >= 10:
        level = 'high'
    elif risk_score >= 5:
        level = 'medium'
    else:
        level = 'low'

    return {
        'risk_score': risk_score,
        'risk_level': level,
        'flags': flags
    }
