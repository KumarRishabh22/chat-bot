import os
from twilio.twiml.voice_response import VoiceResponse, Gather
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
    try:
        response = VoiceResponse()
        gather = Gather(
            input='dtmf speech',
            action='/webhook/voice',
            language='en-US',
            timeout=3,
            numDigits=1
        )
        gather.say("Welcome to our AI helpline. Press any key or start speaking to begin.")
        response.append(gather)

        # Fallback if no input received
        response.redirect('/webhook/voice')
        return response
    except Exception as e:
        logger.error(f"Error creating initial greeting: {str(e)}")
        return create_error_response()

def create_voice_response(text_response):
    try:
        response = VoiceResponse()
        gather = Gather(
            input='dtmf speech',
            action='/webhook/voice',
            language='en-US',
            timeout=3,
            numDigits=1
        )

        # First play/say the response
        gather.say(text_response)
        # Then prompt for next input
        gather.say("Press any key or speak to continue.")
        response.append(gather)

        # Fallback if no input received
        response.redirect('/webhook/voice')
        return response
    except Exception as e:
        logger.error(f"Error creating voice response: {str(e)}")
        return create_error_response()

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
            'from': call.from_formatted,
            'to': call.to_formatted,
            'duration': call.duration,
            'status': call.status,
            'start_time': call.start_time.isoformat() if call.start_time else None
        } for call in calls]
    except Exception as e:
        logger.error(f"Error fetching call logs: {str(e)}")
        return []

# Initialize Twilio client on module import
init_twilio()