import os
import requests
from utils.logger import setup_logger

logger = setup_logger()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # default voice
API_BASE_URL = "https://api.elevenlabs.io/v1"

def text_to_speech(text):
    if not ELEVENLABS_API_KEY:
        logger.warning("ElevenLabs API key not found. Using fallback TTS response.")
        return None

    try:
        url = f"{API_BASE_URL}/text-to-speech/{ELEVENLABS_VOICE_ID}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            logger.error(f"ElevenLabs API error: {response.text}")
            return None

        # Save audio to a publicly accessible URL or cloud storage
        # For this example, we'll assume the response includes a URL
        # In practice, you'd need to implement proper audio file storage
        return response.json().get('audio_url')

    except Exception as e:
        logger.error(f"Text-to-speech conversion failed: {str(e)}")
        return None