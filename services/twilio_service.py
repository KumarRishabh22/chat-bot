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
    response = VoiceResponse()
    if not client:
        response.say("I apologize, but our voice service is currently unavailable. Please try again later.")
        response.hangup()
    else:
        # Configure Gather for both speech and DTMF input
        gather = Gather(
            input='dtmf speech',  # Accept both keypad and voice input
            action='/webhook/voice',
            language='en-US',
            speechTimeout='auto',
            numDigits=1,  # Accept a single digit
            timeout=3,     # Wait 3 seconds for DTMF input
            enhanced=True
        )
        gather.say("Hello! Thank you for calling our customer support. You can speak your question or press any key to continue.")
        response.append(gather)

        # Add a fallback if no input is received
        response.say("I didn't catch that. Please try speaking again or press any key.")
        response.redirect('/webhook/voice')
    return response

def create_voice_response(audio_url):
    response = VoiceResponse()
    gather = Gather(
        input='dtmf speech',  # Accept both keypad and voice input
        action='/webhook/voice',
        language='en-US',
        speechTimeout='auto',
        numDigits=1,
        timeout=3,
        enhanced=True
    )

    if not audio_url:
        gather.say("I apologize, but I'm having trouble generating a response. Please speak again or press any key to continue.")
    else:
        gather.play(audio_url)
        gather.say("Please speak your next question or press any key to continue.")

    response.append(gather)

    # Add a fallback if no input is received
    response.say("I didn't catch that. Please try speaking again or press any key.")
    response.redirect('/webhook/voice')
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