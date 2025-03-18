import os
from twilio.rest import Client
import logging

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

        # Create a call using the application's webhook
        call = client.calls.create(
            url="http://0.0.0.0:5000/webhook/voice",  # Our application's webhook
            to=to_number,  # The number to call
            from_="+14632595522"  # Your Twilio number
        )
        logger.info(f"Call initiated! SID: {call.sid}")
        return call.sid
    except Exception as e:
        logger.error(f"Error making test call: {str(e)}")
        return None

if __name__ == "__main__":
    # Test different language scenarios
    test_scenarios = [
        {
            "number": "+918271523471",  # Your test number
            "description": "Testing English support"
        }
    ]

    for scenario in test_scenarios:
        logger.info(f"Running test scenario: {scenario['description']}")
        call_sid = make_test_call(scenario['number'])
        if call_sid:
            logger.info(f"Test call successful - SID: {call_sid}")
        else:
            logger.error("Test call failed")