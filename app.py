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
        # Get the caller's input
        caller_input = request.values.get('SpeechResult')
        call_sid = request.values.get('CallSid')

        logger.info(f"Received call with SID: {call_sid}")
        logger.info(f"Caller input: {caller_input}")

        if not caller_input:
            # Initial greeting for new calls
            logger.info("Sending initial greeting")
            response = twilio_service.create_initial_greeting()
            return str(response)

        # Process speech input
        text_response = openai_service.process_query(caller_input)
        logger.info(f"Generated response: {text_response}")

        # Convert response to speech
        audio_url = elevenlabs_service.text_to_speech(text_response)
        logger.info(f"Generated audio URL: {audio_url}")

        # Create TwiML response with the audio
        response = twilio_service.create_voice_response(audio_url)

        logger.info(f"Processed call {call_sid} with input: {caller_input}")
        return str(response)

    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        error_response = twilio_service.create_error_response()
        return str(error_response)

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