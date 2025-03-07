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

    # Check if
