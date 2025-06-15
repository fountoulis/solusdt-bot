# webhook_server.py (simple debug version)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("✅ RECEIVED DATA:")
    print(data)
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    print("🚀 Webhook server τρέχει στο http://localhost:5000/webhook")
    app.run(host='0.0.0.0', port=5000)
