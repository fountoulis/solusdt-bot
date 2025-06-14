# webhook_server.py
from flask import Flask, request, jsonify
import json
import threading
import math
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

def calculate_risk(entry, sl):
    return abs(entry - sl)

def calculate_position_size(risk, capital=1000, max_risk_pct=0.10, leverage=5):
    risk_per_trade = capital * max_risk_pct / leverage
    return round(risk_per_trade / risk, 2)

def process_signal(data):
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

    logging.info("📥 ΝΕΟ ΣΗΜΑ ΑΠΟ TRADINGVIEW")
    logging.info(f"📈 Σύμβολο: {symbol} | Κατεύθυνση: {side.upper()}")
    logging.info(f"📍 Entry: {entry} | SL: {sl} | ATR: {atr}")
    logging.info(f"🎯 TP1: {tp1} | TP2: {tp2} | TP3: {tp3} | TP4: {tp4}")
    logging.info(f"📊 RR1: {rr1} | RR2: {rr2}")
    logging.info(f"💰 Μέγεθος Θέσης: {size} SOL")
    logging.info("📉 Trailing SL ενεργοποιείται μετά το TP2 στο 1%")
    logging.info("⚠️ Force Exit: αν εμφανιστεί κερί με body >1.5xATR και close κάτω από προηγούμενο (σε long)")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "no data received"}), 400

    try:
        logging.info(f"✅ Webhook signal received: {data}")
        threading.Thread(target=process_signal, args=(data,)).start()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    logging.info("🚀 Webhook server τρέχει στο http://localhost:5000/webhook")
    app.run(host='0.0.0.0', port=5000)
