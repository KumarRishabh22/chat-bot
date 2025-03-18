# AI Helpline Chatbot Testing Guide

## 1. Dashboard Access
1. The application is running at: http://0.0.0.0:5000/
2. You should see:
   - Recent calls table
   - Statistics panel showing total calls and average duration
   - Real-time updates every 30 seconds

## 2. Testing Voice Calls
### Prerequisites
1. Ensure you have a Twilio phone number configured
2. Use the Twilio console (https://console.twilio.com) to:
   - Configure your webhook URL as: `http://your-repl-url/webhook/voice`
   - Set the webhook method to POST

### Testing Steps
1. Call your Twilio phone number
2. You should hear the initial greeting
3. Speak your query in any supported language
4. The bot should respond with:
   - AI-generated response using OpenAI
   - Natural voice using ElevenLabs

## 3. Testing Multi-language Support
Currently supported languages:
- English (US) - `en-US`
- Spanish (Spain) - `es-ES`
- French (France) - `fr-FR`

To test:
1. Call the helpline
2. Speak in any supported language
3. The system should:
   - Detect the language automatically
   - Respond in the same language
   - Show the correct language in call logs

## 4. Database Testing
The application uses PostgreSQL to store:
- Call logs
- Product information (with translations)
- Order status
- Supported languages

To verify database content:
1. Check the dashboard for call history
2. Monitor the logs in the Replit console
3. New calls should appear in real-time

## Common Test Scenarios
1. Product Inquiry:
   - Call and ask: "What headphones do you have?"
   - Expected: Description of Premium Headphones in your language

2. Order Status:
   - Call and ask: "Where is my order ORD001?"
   - Expected: Status and delivery date for the order

3. Language Switching:
   - Start in English, then switch to Spanish
   - Bot should adapt to the language change

## Troubleshooting
If you encounter issues:
1. Check the Replit console for error logs
2. Verify all API keys are properly set:
   - OPENAI_API_KEY
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - ELEVENLABS_API_KEY
3. Ensure the PostgreSQL database is running
