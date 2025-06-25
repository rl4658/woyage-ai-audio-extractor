# Woyage AI Audio Extractor (Web)

## Setup

1. `git clone … && cd woyage-ai-audio-extractor`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Fill in `.env` with your AWS creds.
5. `uvicorn app.main:app --reload`

Open http://127.0.0.1:8000 in your browser.  
