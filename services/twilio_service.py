import os
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import logging

logger = logging.getLogger('helpline_bot')

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

client = None

def init_twilio():
    global client
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        return True
    logger.warning("Twilio credentials not found. Call handling features will be limited.")
    return False

def create_initial_greeting():
    response = VoiceResponse()
    if not client:
        response.say("I apologize, but our voice service is currently unavailable. Please try again later.")
        response.hangup()
    else:
        response.say("Hello! Thank you for calling our customer support. How can I assist you today?")
        response.gather(
            input='speech',
            action='/webhook/voice',
            language='en-US',
            speechTimeout='auto'
        )
    return response

def create_voice_response(audio_url):
    response = VoiceResponse()
    if not audio_url:
        response.say("I apologize, but I'm having trouble generating a response. Please try again later.")
    else:
        response.play(audio_url)
    response.gather(
        input='speech',
        action='/webhook/voice',
        language='en-US',
        speechTimeout='auto'
    )
    return response

def create_error_response():
    response = VoiceResponse()
    response.say("I apologize, but I'm having trouble processing your request. Please try again later.")
    response.hangup()
    return response

def get_call_logs():
    if not client:
        logger.warning("Cannot fetch call logs: Twilio client not initialized")
        return []
    try:
        calls = client.calls.list(limit=50)
        return [{
            'call_sid': call.sid,
            'from': call.from_,
            'to': call.to,
            'duration': call.duration,
            'status': call.status,
            'start_time': call.start_time.isoformat() if call.start_time else None
        } for call in calls]
    except Exception as e:
        logger.error(f"Error fetching call logs: {str(e)}")
        return []

# Initialize Twilio client on module import
init_twilio()