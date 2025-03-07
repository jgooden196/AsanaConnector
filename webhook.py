from flask import Flask, request, jsonify

app = Flask(__name__)

WEBHOOK_SECRET = {}

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Handle Asana's webhook handshake
    if 'X-Hook-Secret' in request.headers:
        secret = request.headers['X-Hook-Secret']
        WEBHOOK_SECRET['secret'] = secret  # Store secret dynamically
        response = jsonify({})
        response.headers['X-Hook-Secret'] = secret
        return response, 200

    # Process incoming webhook event
    data = request.json
    print("Received Asana Event:", data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
