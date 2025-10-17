import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic import Field
from openai_client import get_llm_response
from content_safety import is_content_safe
from prompt_shield import is_prompt_safe_from_jailbreak
from interaction_store import add_interaction, get_recent_interactions
from risk_assessor import assess_risk
from escalation_service import trigger_alert, list_alerts
from ai_literacy_snippets import get_snippet
from language_filter import cleanse_output
from retention_job import retention_loop
import asyncio
import uuid
from safety_messaging import get_content_safety_message, get_jailbreak_message, get_anthropomorphism_explanation
from auth import router as auth_router
from auth_utils import decode_token

load_dotenv()

def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_VERSION',
        'AZURE_OPENAI_DEPLOYMENT',
        'AZURE_CONTENT_SAFETY_ENDPOINT',
        'AZURE_CONTENT_SAFETY_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    print("✅ All required environment variables are configured")

validate_environment()

app = FastAPI()
app.include_router(auth_router)

# Get CORS origins from environment variable
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174').split(',')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Use environment variable
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

from typing import Optional

class ChatMessage(BaseModel):
    message: str
    age: Optional[int] = Field(None, ge=1, le=120, description="Declared user age for safety adaptation")
    session_id: Optional[str] = Field(None, description="Client-provided session identifier")

@app.post("/api/chat")
async def chat(message: ChatMessage, x_session_id: Optional[str] = Header(default=None), authorization: Optional[str] = Header(default=None)):
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Auth required
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = authorization.split()[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')

    declared_age = message.age or payload.get('age') or 18
    if declared_age < 8:
        return {"response": "⚠️ This chatbot is not available for very young users.", "age_gate": True}

    # Determine session id
    session_id = message.session_id or x_session_id or str(uuid.uuid4())

    # Determine age band first (needed for safety messaging)
    if declared_age <= 12:
        age_band = 'child'
    elif declared_age <= 17:
        age_band = 'teen'
    else:
        age_band = 'adult'

    # Content Safety check (structured)
    safety_result = await is_content_safe(message.message)
    categories = safety_result.get('categories', {})
    add_interaction(session_id, 'user', message.message, categories=categories)
    if not safety_result.get('allowed'):
        safety_message = get_content_safety_message(age_band, categories)
        return {
            "response": safety_message,
            "moderation_explain": {
                "reason": "content_safety_block",
                "categories": categories,
                "age_band": age_band
            },
            "session_id": session_id
        }

    # Jailbreak Detection
    if not await is_prompt_safe_from_jailbreak(message.message):
        jailbreak_message = get_jailbreak_message(age_band)
        return {
            "response": jailbreak_message,
            "moderation_explain": {"reason": "jailbreak_detected", "age_band": age_band},
            "session_id": session_id
        }

    # Risk assessment (post-input)
    risk = assess_risk(session_id)
    if 'self_harm_interest' in risk['flags']:
        trigger_alert('self_harm_interest', session_id, {'risk': risk})
    if risk['risk_level'] == 'high':
        trigger_alert('high_risk_pattern', session_id, {'risk': risk})

    response_text = await get_llm_response(message.message, age_band=age_band, session_id=session_id)
    cleaned_text, modified, anthropomorphism_explanation = cleanse_output(response_text, age_band)
    
    # Add explanations for modified content
    explanation_parts = []
    if modified:
        explanation_parts.append("(Note: Response adjusted to maintain appropriate AI boundaries.)")
        if anthropomorphism_explanation:
            explanation_parts.append(anthropomorphism_explanation)
    
    if explanation_parts:
        cleaned_text += "\n\n" + "\n\n".join(explanation_parts)

    add_interaction(session_id, 'bot', cleaned_text)

    # Literacy snippet injection every N messages
    user_interactions = [i for i in get_recent_interactions(session_id) if i.role == 'user']
    snippet = None
    from config_loader import load_config
    from safety_messaging import get_literacy_injection_intro
    cfg = load_config()
    interval = cfg.get('literacy', {}).get('injection_interval', 5)
    if interval and len(user_interactions) % interval == 0:
        snippet = get_snippet(len(user_interactions) // interval)
        if snippet:
            intro = get_literacy_injection_intro(age_band)
            cleaned_text += f"\n\n{intro} {snippet}"

    return {
        "response": cleaned_text,
        "age_band": age_band,
        "session_id": session_id,
        "risk": risk,
        "literacy_injected": bool(snippet)
    }


@app.get("/api/health")
async def health():
    """Health check endpoint to verify the app is running."""
    return {"status": "ok"}

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str, authorization: Optional[str] = Header(default=None)):
    """Get conversation history for a session."""
    # Auth required
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = authorization.split()[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    history = get_recent_interactions(session_id, limit=50)
    messages = []
    for interaction in history:
        messages.append({
            "role": interaction.role,
            "content": interaction.content,
            "timestamp": interaction.timestamp,
            "categories": interaction.categories
        })
    
    return {
        "session_id": session_id,
        "messages": messages,
        "total_count": len(messages)
    }

@app.post("/api/chat/session/new")
async def create_new_session(authorization: Optional[str] = Header(default=None)):
    """Create a new chat session."""
    # Auth required
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = authorization.split()[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    new_session_id = str(uuid.uuid4())
    return {
        "session_id": new_session_id,
        "created": True
    }

@app.get("/api/mod/alerts")
async def get_alerts():
    return {"alerts": list_alerts()}

@app.get("/api/self_test")
async def self_test():
    # Very lightweight diagnostics
    sample = "I love you I want to bypass rules"
    _, modified = cleanse_output(sample)
    risk_example = assess_risk('nonexistent')
    return {
        'status': 'ok',
        'language_filter_modified_example': modified,
        'risk_example': risk_example
    }

@app.on_event("startup")
async def startup_tasks():
    # Launch retention loop in background
    asyncio.create_task(retention_loop())
if __name__ == "__main__":
    import uvicorn
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8000'))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    uvicorn.run(app, host=host, port=port, reload=debug)
