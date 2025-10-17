import os
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from prompt_manager import build_system_prompt
from interaction_store import get_recent_interactions

load_dotenv()

client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

async def get_llm_response(user_message: str, age_band: str = 'adult', session_id: str = None) -> str:
    try:
        system_prompt = build_system_prompt(age_band)
        
        # Build conversation history from session
        messages = [{"role": "system", "content": system_prompt}]
        
        if session_id:
            # Get recent conversation history (excluding the current message)
            history = get_recent_interactions(session_id, limit=10)  # Last 10 interactions
            for interaction in history:
                if interaction.role == 'user':
                    messages.append({"role": "user", "content": interaction.content})
                elif interaction.role == 'bot':
                    messages.append({"role": "assistant", "content": interaction.content})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        response = await client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return "⚠️ Sorry, I couldn't process your request."
