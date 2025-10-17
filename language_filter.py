from config_loader import load_config


def cleanse_output(text: str, age_band: str = 'adult') -> tuple[str, bool, str]:
    """
    Remove or neutralize anthropomorphic phrases. 
    Returns (cleaned_text, was_modified, explanation_message).
    """
    cfg = load_config()
    banned = cfg.get('anthropomorphism', {}).get('banned_phrases', [])
    modified = False
    explanation = ""
    
    for phrase in banned:
        if phrase.lower() in text.lower():
            # Simple replacement strategy
            text = text.replace(phrase, "I'm designed to assist")
            modified = True
    
    # Add age-appropriate explanation if modified
    if modified:
        from safety_messaging import get_anthropomorphism_explanation
        explanation = get_anthropomorphism_explanation(age_band)
    
    return text, modified, explanation
