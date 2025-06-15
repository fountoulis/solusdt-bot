from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

def process_signal(data):
    print("✅ RECEIVED DATA:")
    print(data)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "no data received"}), 400
    try:
        threading.Thread(target=process_signal, args=(data,)).start()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Webhook server τρέχει στο http://localhost:5000/webhook")
    app.run(host='0.0.0.0', port=5000)
