import os
from twilio.rest import Client
import logging
import urllib.parse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_test_call(to_number):
    try:
        # Use environment variables for security
        client = Client(
            os.environ.get("TWILIO_ACCOUNT_SID"),
            os.environ.get("TWILIO_AUTH_TOKEN")
        )

        # Get the Replit URL from environment
        replit_url = os.environ.get('REPL_SLUG', '')
        webhook_url = f"https://{replit_url}.replit.dev/webhook/voice"

        logger.info(f"Using webhook URL: {webhook_url}")

        # Format the phone number with country code if not present
        if not to_number.startswith('+'):
            to_number = f"+91{to_number}"  # Add India country code

        # Create a call using the application's webhook
        call = client.calls.create(
            url=webhook_url,  # Use the public Replit URL
            to=to_number,     # The number to call
            from_="+14632595522"  # Your Twilio number
        )
        logger.info(f"Call initiated! SID: {call.sid}")
        return call.sid
    except Exception as e:
        logger.error(f"Error making test call: {str(e)}")
        return None

if __name__ == "__main__":
    # Test call to your number
    test_number = "8271523471"  # Will be formatted to +918271523471
    logger.info(f"Making test call to: {test_number}")
    call_sid = make_test_call(test_number)

    if call_sid:
        logger.info(f"Test call successful - SID: {call_sid}")
    else:
        logger.error("Test call failed")