# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **WhatsApp OpenAI Assistant** that creates a direct integration between WhatsApp (via Twilio) and OpenAI's Assistant API v2 using Python and Flask.

## Core Architecture

1. **Flask Web Server**: Receives webhooks from Twilio for incoming WhatsApp messages
2. **Twilio Integration**: Manages WhatsApp message sending/receiving
3. **OpenAI Assistant v2**: Processes messages and generates intelligent responses
4. **Thread Management**: Maintains conversation context per user phone number

## Essential Commands

### Development
```bash
# Set up development environment
chmod +x setup.sh && ./setup.sh

# Run development server (locally)
python app.py

# Or use the run script
chmod +x run.sh && ./run.sh

# Expose local server for webhook testing
ngrok http 5000
```

### Deployment (Render)
```bash
# Uses start.sh script which handles PORT environment variable
./start.sh

# Health check endpoint
curl http://localhost:5000/health
```

### Virtual Environment
```bash
# Create virtual environment
python3.10 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Key Files & Their Purpose

- **app.py**: Main Flask application with webhook endpoint and OpenAI integration
- **gunicorn_config.py**: Production server configuration (port 10000 for Render)
- **requirements.txt**: Python dependencies including flask, twilio, openai
- **render.yaml**: Render deployment configuration
- **.env**: Environment variables (not committed to repo)
- **ai_docs/**: Project documentation and API integration details

## Environment Variables

Required environment variables:
- `TWILIO_ACCOUNT_SID`: Twilio account identifier
- `TWILIO_AUTH_TOKEN`: Twilio authentication token
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_ASSISTANT_ID`: ID of your OpenAI Assistant
- `PORT`: Server port (default: 5000 for Render)
- `DEBUG`: Debug mode flag (True/False)

## API Integration Details

### OpenAI Assistant v2
- Must include header: `"OpenAI-Beta": "assistants=v2"`
- Uses GPT-4o model for better performance
- Thread-based conversation management
- Run status monitoring for response retrieval

### Twilio WhatsApp
- Webhook endpoint: `/webhook`
- Expects POST requests with `Body` and `From` parameters
- Returns TwiML formatted responses
- Supports template messages for initiating conversations

## Important Considerations

1. **Thread Storage**: Currently uses in-memory dictionary - requires database for production
2. **Error Handling**: Implements safety for TypeError with 'proxies' argument in OpenAI client initialization
3. **Port Configuration**: Render uses PORT environment variable (defaults to 5000)
4. **Health Check**: `/health` endpoint for service monitoring
5. **Timeout Settings**: 5-minute timeout configured in gunicorn for long operations

## Common Development Tasks

### Adding a New Feature
1. Check existing patterns in app.py
2. Maintain thread management structure
3. Follow Flask response format with TwiML
4. Add appropriate error handling

### Debugging
- Check Flask logs for incoming messages
- Monitor OpenAI run status
- Verify environment variables are loaded
- Use ngrok web interface to inspect webhooks

### Testing
- Manual testing with WhatsApp Sandbox
- Check health endpoint: `curl http://localhost:5000/health`
- Monitor logs during message processing