# Safe LLM Bot with React Frontend

This project consists of a Python FastAPI backend that provides a safe LLM chat interface using Azure OpenAI and Azure Content Safety, and a React frontend for the chat interface.

## Project Structure

```
.
├── frontend/          # React frontend application
└── backend/          # Python FastAPI backend
    ├── app.py        # Main FastAPI application
    ├── content_safety.py  # Content safety checking
    └── openai_client.py   # OpenAI client configuration
```

## Setup

### Backend

1. **Create and activate a virtual environment:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

2. **Set up environment variables:**
Copy the example environment file and fill in your Azure credentials:
```bash
cp .env.example .env
```

Edit the `.env` file with your Azure credentials:
```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment
AZURE_CONTENT_SAFETY_ENDPOINT=your_endpoint
AZURE_CONTENT_SAFETY_KEY=your_key
JWT_SECRET=your_secure_jwt_secret
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the backend:**
```bash
# Using uvicorn directly
uvicorn app:app --reload

# Or using Python
python app.py
```

The backend will be available at http://localhost:8000.

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173 and will connect to the backend at http://localhost:8000.

## Features

- Real-time chat interface
- Azure Content Safety text moderation & jailbreak detection
- Age-adaptive system prompts (child / teen / adult bands)
- Risk heuristics & escalation alert queue (Phase 2)
- Literacy tip injection every N interactions
- Anthropomorphism phrase filtering
- JWT authentication (register / login / profile)
- Persistent session id for longitudinal safety analysis
- Modern UI with Chakra UI & React Router
- TypeScript support
- Fully asynchronous backend

## Authentication

Endpoints (JSON):

| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/auth/register | Create user (username, password, age optional) |
| POST | /api/auth/login | Obtain JWT access token |
| GET | /api/auth/me | Retrieve current user profile |
| POST | /api/chat | Authenticated chat (Bearer token required) |

Include the JWT as:

```
Authorization: Bearer <token>
```

Age gating & prompt tailoring use the `age` claim embedded at registration.

## Safety Enhancements (Summary)

- Multi-layer moderation: content safety → jailbreak → risk assessment → output cleanse.
- Interaction store (in-memory) keeps rolling context (no PII persistence by design).
- Configurable retention & anthropomorphism lists via `safety_config.yaml`.
- Self-test endpoint `/api/self_test` for quick diagnostics.

## UX Safety Cues

- Centered chat panel with scrollable history pane and sticky input.
- Age band banner (child / teen / adult) showing tailored safety wording.
- Badges: `adjusted` (content normalized), `tip` (AI literacy snippet), `high/medium risk` (heuristic flags).
- Safety notices appear under messages when blocked or transformed with category details tooltip.
- Auto-scroll only when near bottom; floating new-message button otherwise.
- Typing indicator bubble while awaiting model response.
- Copy-to-clipboard button on assistant messages.
- Screen-reader friendly live region for new messages.