# webhook_server.py
from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def calculate_risk(entry, sl):
    return abs(entry - sl)

def calculate_position_size(risk, capital=1000, max_risk_pct=0.10, leverage=5):
    risk_per_trade = capital * max_risk_pct / leverage
    return round(risk_per_trade / risk, 2)

def process_signal(data):
    print("✅ RECEIVED DATA:")
    print(data)

    symbol = data.get("symbol")
    side = data.get("side")
    entry = float(data.get("entry"))
    sl = float(data.get("sl"))
    tp1 = float(data.get("tp1"))
    tp2 = float(data.get("tp2"))
    tp3 = float(data.get("tp3"))
    tp4 = float(data.get("tp4"))
    atr = float(data.get("atr"))

    risk = calculate_risk(entry, sl)
    rr1 = round((tp1 - entry) / risk, 2) if side == "buy" else round((entry - tp1) / risk, 2)
    rr2 = round((tp2 - entry) / risk, 2) if side == "buy" else round((entry - tp2) / risk, 2)
    size = calculate_position_size(risk)

    print("\n🚀 ΝΕΟ ΣΗΜΑ ΑΠΟ TRADINGVIEW!")
    print(f"🔸 Σύμβολο: {symbol} | Κατεύθυνση: {side.upper()}")
    print(f"📍 Είσοδος: {entry} | SL: {sl} | ATR: {atr}")
    print(f"🎯 TP1: {tp1} | TP2: {tp2} | TP3: {tp3} | TP4: {tp4}")
    print(f"📈 RR1: {rr1} | RR2: {rr2}")
    print(f"💰 Μέγεθος Θέσης: {size} SOL")
    print("🔄 Trailing SL ενεργοποιείται μετά το TP2 στο 1%")
    print("⚠️ Force Exit: αν εμφανιστεί κερί με body >1.5xATR και close κάτω από προηγούμενο (σε long)")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "no data received"}), 400
    try:
        print("✅ RECEIVED DATA:")
        print(data)
        process_signal(data)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Webhook server τρέχει στο http://localhost:5000/webhook")
    app.run(host='0.0.0.0', port=5000)
