import logging
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging to ensure Railway logs appear
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

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
    app.run(host='0.0.0.0', port=5000)
