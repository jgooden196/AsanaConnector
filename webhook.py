import logging
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging to ensure Railway logs appear
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

WEBHOOK_SECRET = {}

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Handle Asana's webhook handshake
    if 'X-Hook-Secret' in request.headers:
        secret = request.headers['X-Hook-Secret']
        WEBHOOK_SECRET['secret'] = secret  # Store secret dynamically
        response = jsonify({})
        response.headers['X-Hook-Secret'] = secret
        logger.info(f"Webhook Handshake Successful: {secret}")
        sys.stdout.flush(
