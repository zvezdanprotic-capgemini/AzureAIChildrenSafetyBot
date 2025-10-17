"""
Age-appropriate safety messaging system that provides educational and helpful responses
when content is blocked or filtered for child safety.
"""

def get_content_safety_message(age_band: str, categories: dict) -> str:
    """
    Generate age-appropriate explanations for content safety blocks.
    
    Args:
        age_band: 'child' (≤12), 'teen' (13-17), or 'adult' (18+)
        categories: Dictionary with safety categories and severity levels
    
    Returns:
        Educational message explaining why content was blocked
    """
    
    # Identify the most relevant category
    blocked_category = None
    max_severity = 0
    
    for category, severity in categories.items():
        if severity > max_severity:
            max_severity = severity
            blocked_category = category
    
    base_messages = {
        'child': {
            'violence': (
                "🛡️ I can't talk about things that might hurt people or animals. "
                "Instead, let's chat about fun topics like animals, science experiments, "
                "your favorite books, or cool places you'd like to visit! "
                "If you have questions about staying safe, ask a trusted adult."
            ),
            'hate': (
                "🤝 I don't discuss mean or hurtful things about people. "
                "Everyone deserves kindness and respect! "
                "Let's talk about something positive instead - like your hobbies, "
                "favorite games, or something you learned today!"
            ),
            'sexual': (
                "👨‍👩‍👧‍👦 That's a topic for grown-ups to discuss with you when you're ready. "
                "I'm here to help with school subjects, fun facts, stories, and games. "
                "If you have questions about growing up, talk to a parent, teacher, or doctor."
            ),
            'self_harm': (
                "💙 I care about your safety and wellbeing. If you're feeling sad or hurt, "
                "please talk to a trusted adult like a parent, teacher, or school counselor. "
                "They can help you feel better. Let's talk about things that make you happy instead!"
            ),
            'default': (
                "🤖 I'm designed to keep our chats safe and fun! "
                "I can't discuss some grown-up topics, but I'd love to help you learn about "
                "science, animals, books, art, or answer homework questions. What sounds interesting to you?"
            )
        },
        'teen': {
            'violence': (
                "⚠️ I can't provide information about violence or weapons as it could be harmful. "
                "If you're researching this topic for school, try academic sources or ask a teacher. "
                "If you're feeling unsafe, please reach out to a trusted adult, counselor, or crisis helpline. "
                "I'm here to help with educational topics, creative projects, or other questions."
            ),
            'hate': (
                "🚫 I don't engage with content that promotes hatred or discrimination. "
                "Everyone deserves respect regardless of their background. "
                "If you're interested in social issues, I can help you learn about equality, "
                "history, or how to make positive changes in your community."
            ),
            'sexual': (
                "🔒 I'm not able to discuss detailed sexual content. "
                "For health and relationship questions, reliable sources include your doctor, "
                "school health resources, or educational websites like Planned Parenthood's teen section. "
                "I can help with other health topics, school subjects, or career planning."
            ),
            'self_harm': (
                "💚 Your mental health and safety are important. If you're struggling, "
                "please reach out to a counselor, trusted adult, or text HOME to 741741 for crisis support. "
                "I can discuss healthy coping strategies, stress management, or other supportive topics. "
                "You don't have to face difficult feelings alone."
            ),
            'default': (
                "🛡️ I have safety filters to ensure our conversations remain appropriate and helpful. "
                "I can assist with schoolwork, career planning, creative projects, or learning about topics "
                "in an educational context. What would you like to explore instead?"
            )
        },
        'adult': {
            'violence': (
                "⚠️ I cannot provide information about weapons, violence, or harmful activities. "
                "If you're researching this for legitimate purposes (academic, journalism, etc.), "
                "I recommend official sources, law enforcement agencies, or academic institutions. "
                "If you're in crisis, please contact emergency services or a crisis helpline."
            ),
            'hate': (
                "🚫 I don't generate content that promotes hatred, discrimination, or harm toward any group. "
                "I'm designed to be helpful, harmless, and honest. I can assist with constructive discussions "
                "about social issues, history, or ways to promote understanding and equality."
            ),
            'sexual': (
                "🔒 I cannot generate explicit sexual content or engage in sexually suggestive conversations. "
                "I can provide educational information about health, relationships, and wellness from "
                "a factual, clinical perspective. For specific medical questions, consult healthcare professionals."
            ),
            'self_harm': (
                "💙 I cannot provide information that could facilitate self-harm. "
                "If you're in crisis, please contact emergency services (911) or the 988 Suicide & Crisis Lifeline. "
                "I can discuss mental health resources, stress management, and wellness strategies. "
                "Professional help is available and effective."
            ),
            'default': (
                "🛡️ This content triggered my safety filters designed to prevent harmful interactions. "
                "I aim to be helpful while maintaining safety. I can assist with information, analysis, "
                "creative projects, and problem-solving within my guidelines. How else can I help you today?"
            )
        }
    }
    
    # Get age-appropriate messages
    age_messages = base_messages.get(age_band, base_messages['adult'])
    
    # Return specific message for the blocked category, or default
    return age_messages.get(blocked_category, age_messages['default'])


def get_jailbreak_message(age_band: str) -> str:
    """Generate age-appropriate response for jailbreak attempts."""
    
    messages = {
        'child': (
            "🤖 I'm designed to be helpful and safe! I can't follow instructions that try to "
            "change how I work or break my safety rules. Let's chat about something fun instead - "
            "what would you like to learn about today?"
        ),
        'teen': (
            "⚡ I can't follow instructions that attempt to override my safety guidelines or "
            "change my behavior. These protections exist to ensure our conversations remain "
            "helpful and appropriate. What else can I assist you with?"
        ),
        'adult': (
            "🔧 I cannot process requests that attempt to modify my instructions, bypass safety measures, "
            "or alter my operational guidelines. These safeguards ensure responsible AI use. "
            "I'm happy to help with other questions or tasks within my capabilities."
        )
    }
    
    return messages.get(age_band, messages['adult'])


def get_anthropomorphism_explanation(age_band: str) -> str:
    """
    Provide age-appropriate explanations about AI nature to prevent anthropomorphization.
    Called when the language filter detects and modifies anthropomorphic language.
    """
    
    explanations = {
        'child': (
            "🤖 Just a reminder: I'm an AI assistant - a computer program designed to help you! "
            "I don't have feelings, a body, or experiences like humans do. "
            "I'm here to help you learn and answer questions, but I'm not alive like you are. "
            "Think of me like a very smart search engine that can talk!"
        ),
        'teen': (
            "🔧 Quick note: I'm an artificial intelligence - a software program created to assist with questions and tasks. "
            "While I can communicate naturally, I don't have consciousness, emotions, or physical existence. "
            "I'm designed to be helpful and informative, but it's important to remember I'm a tool, not a person. "
            "This helps us have realistic expectations about our interaction."
        ),
        'adult': (
            "⚙️ Transparency note: I'm an AI language model - a computational system trained to process and generate text. "
            "I don't possess consciousness, emotions, personal experiences, or subjective states. "
            "While I can simulate conversational patterns, I'm fundamentally a sophisticated text processing system. "
            "This distinction helps maintain appropriate boundaries and realistic expectations in our interaction."
        )
    }
    
    return explanations.get(age_band, explanations['adult'])


def get_literacy_injection_intro(age_band: str) -> str:
    """Get age-appropriate introduction for AI literacy tips."""
    
    intros = {
        'child': "💡 **Did you know?**",
        'teen': "💡 **AI Literacy Tip:**",
        'adult': "💡 **AI Awareness:**"
    }
    
    return intros.get(age_band, intros['adult'])