import os
import logging
import sys
from flask import Flask, request, jsonify
from asana import Client

app = Flask(__name__)

# Configure logging to ensure Railway logs appear
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

# Asana API setup
asana_token = os.environ.get('ASANA_TOKEN')
client = Client.access_token(asana_token)

# Your Asana project ID
project_id = '1209353707682767'

# Dictionary to store webhook secret dynamically
WEBHOOK_SECRET = {}

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handles incoming webhook requests from Asana"""

    # Check if this is the webhook handshake request
    if 'X-Hook-Secret' in request.headers:
        secret = request.headers['X-Hook-Secret']
        WEBHOOK_SECRET['secret'] = secret  # Store secret dynamically
        
        response = jsonify({})
        response.headers['X-Hook-Secret'] = secret  # Send back the secret
         
        logger.info(f"Webhook Handshake Successful. Secret: {secret}")
        sys.stdout.flush()  # Ensure logs appear immediately

        return response, 200

    # If it's not a handshake, it's an event
    data = request.json
    logger.info(f"Received Asana Event: {data}")
    sys.stdout.flush()  # Ensure logs appear

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
