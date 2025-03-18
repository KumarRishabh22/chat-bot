import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///helpline.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Import routes after app initialization to avoid circular imports
from services import twilio_service, openai_service, elevenlabs_service
from utils.logger import setup_logger

# Setup logging
logger = setup_logger()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/webhook/voice', methods=['POST'])
def handle_incoming_call():
    try:
        # Log all request data for debugging
        logger.info("Incoming webhook request data:")
        logger.info(f"Request values: {request.values}")

        # Get call data
        dtmf_input = request.values.get('Digits')
        speech_input = request.values.get('SpeechResult')
        call_sid = request.values.get('CallSid')

        logger.info(f"Call SID: {call_sid}")
        logger.info(f"DTMF input: {dtmf_input}")
        logger.info(f"Speech input: {speech_input}")

        # Initial call or no input
        if not speech_input and not dtmf_input:
            logger.info("New call - sending greeting")
            return str(twilio_service.create_initial_greeting())

        # Handle user input (both DTMF and speech)
        user_input = speech_input if speech_input else "How can I help you today?"

        # Generate AI response
        ai_response = openai_service.process_query(user_input)
        logger.info(f"AI response: {ai_response}")

        # Create TwiML response
        response = twilio_service.create_voice_response(ai_response)
        return str(response)

    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}", exc_info=True)
        return str(twilio_service.create_error_response())

@app.route('/calls/log', methods=['GET'])
def get_call_logs():
    try:
        calls = twilio_service.get_call_logs()
        return jsonify(calls)
    except Exception as e:
        logger.error(f"Error fetching call logs: {str(e)}")
        return jsonify({"error": "Failed to fetch call logs"}), 500

# Create all database tables
with app.app_context():
    import models
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)