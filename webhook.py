import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

WEBHOOK_SECRET = {}

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Handle Asana's webhook handshake
    if 'X-Hook-Secret' in request.headers:
        secret = request.headers['X-Hook-Secret']
        WEBHOOK_SECRET['secret'] = secret  # Store secret dynamically
        response = jsonify({})
        response.headers['X-Hook-Secret'] = secret
        logging.info(f"Webhook Handshake Successful: {secret}")
        return response, 200

    # Process incoming webhook event
    data = request.json
    logging.info(f"Received Asana Event: {data}")  # Force log output
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
