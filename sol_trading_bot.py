# sol_trading_bot/webhook_server.py

from flask import Flask, request, jsonify
import json
import math

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    symbol = data.get("symbol")
    side = data.get("side")
    entry = float(data.get("entry"))
    sl = float(data.get("sl"))
    tp1 = float(data.get("tp1"))
    tp2 = float(data.get("tp2"))
    tp3 = float(data.get("tp3"))
    tp4 = float(data.get("tp4"))
    atr = float(data.get("atr"))

    # Υπολογισμός RR ratio για TP1 και TP2
    rr1 = round((tp1 - entry) / abs(entry - sl), 2) if side == "buy" else round((entry - tp1) / abs(entry - sl), 2)
    rr2 = round((tp2 - entry) / abs(entry - sl), 2) if side == "buy" else round((entry - tp2) / abs(entry - sl), 2)

    # Simulate risk calculation (dummy capital and leverage)
    capital = 1000  # USDT
    risk_per_trade = 0.10 * capital
    stop_distance = abs(entry - sl)
    position_size = (risk_per_trade / stop_distance) * 5  # leverage 5x
    position_size = min(position_size, 500)  # max 500 SOL

    print("\n--- 📩 ΝΕΟ ΣΗΜΑ ΑΠΟ TRADINGVIEW ---")
    print(f"🔸 Symbol: {symbol} | Direction: {side.upper()}")
    print(f"🔹 Entry: {entry} | SL: {sl} | ATR: {atr}")
    print(f"🎯 TP1: {tp1} | TP2: {tp2} | TP3: {tp3} | TP4: {tp4}")
    print(f"📏 RR1: {rr1} | RR2: {rr2}")
    print(f"📦 Position Size: {round(position_size, 2)} SOL")

    # Trailing Stop & Force Exit Logic (printed for now)
    print("🟢 Trailing SL ενεργοποιείται μετά το TP1 στο 1% κάτω από market")
    print("🛑 Force Exit αν candle με σώμα >1.5xATR και volume spike")

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
