import os
import json
from openai import OpenAI
from models import Order, Product
import logging

logger = logging.getLogger('helpline_bot')

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = None

def init_openai():
    global client
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        return True
    logger.warning("OpenAI API key not found. Natural language processing features will be limited.")
    return False

def transcribe_audio(audio_file):
    if not client:
        raise Exception("OpenAI client not initialized. Please provide OPENAI_API_KEY.")
    try:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response.text
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {str(e)}")

def process_query(text):
    if not client:
        return "I apologize, but I'm currently unable to process natural language queries. Please try again later."
    try:
        system_message = """You are a helpful customer service AI assistant. 
        Respond to customer queries about orders, products, and general support.
        Keep responses concise and natural-sounding."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            max_tokens=150
        )

        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to process query: {str(e)}")
        return "I apologize, but I'm having trouble understanding. Please try again later."

def get_order_status(order_number):
    try:
        order = Order.query.filter_by(order_number=order_number).first()
        if order:
            return {
                "status": order.status,
                "estimated_delivery": order.estimated_delivery.strftime("%Y-%m-%d")
            }
        return None
    except Exception as e:
        logger.error(f"Error getting order status: {str(e)}")
        return None

# Initialize OpenAI client on module import
init_openai()