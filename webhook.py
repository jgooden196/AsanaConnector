import logging
import sys
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging to ensure Railway logs appear
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

# Environment variables for Asana credentials
ASANA_ACCESS_TOKEN = os.getenv("ASANA_ACCESS_TOKEN")
ASANA_PROJECT_ID = os.getenv("ASANA_PROJECT_ID")

def get_project_tasks():
    """
    Fetch tasks from the Asana project.
    """
    url = f"https://app.asana.com/api/1.0/projects/{ASANA_PROJECT_ID}/tasks"
    headers = {
        "Authorization": f"Bearer {ASANA_ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        logger.error(f"Failed to fetch tasks: {response.text}")
        return None

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming webhook requests from Asana.
    """
    data = request.json

    # Check if it is the webhook handshake request
    if "X-Hook-Secret" in request.headers:
        secret = request.headers["X-Hook-Secret"]
        response = jsonify({})
        response.headers["X-Hook-Secret"] = secret  # Send back the secret
        logger.info(f"Webhook Handshake Successful. Secret: {secret}")
        sys.stdout.flush()  # Ensure logs appear immediately
        return response, 200

    # If it's not a handshake, it's an event
    logger.info(f"Received Asana Event: {data}")
    sys.stdout.flush()  # Ensure logs appear immediately

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
