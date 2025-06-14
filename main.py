

# main.py
import json
import requests
import time
from math import floor

# Load config
with open("config.json") as f:
    config = json.load(f)

API_KEY = config["api_key"]
API_SECRET = config["api_secret"]
BASE_URL = config["base_url"]
LEVERAGE = config["leverage"]
RISK_PERCENT = config["risk_percent"]
MAX_POSITION_SIZE = config["max_position_size"]

# Fake account balance (replace with real call if needed)
ACCOUNT_BALANCE_USDT = 1000

# Example webhook payload for entry
example_signal = {
    "symbol": "SOLUSDT",
    "side": "buy",  # or "sell"
    "entry": 150.00,
    "sl": 148.00,
    "tp1": 155.00,
    "tp2": 157.50,
    "tp3": 159.00,
    "tp4": 160.00,
    "atr": 1.2
}

# === ORDER FUNCTION ===
def place_order(signal):
    side = signal["side"]
    symbol = signal["symbol"]
    entry = float(signal["entry"])
    sl = float(signal["sl"])
    atr = float(signal["atr"])

    # Calculate risk per SOL
    risk_per_unit = abs(entry - sl)
    max_risk = (RISK_PERCENT / 100) * ACCOUNT_BALANCE_USDT
    qty = floor((max_risk / risk_per_unit) * LEVERAGE)

    if qty > MAX_POSITION_SIZE:
        confirm = input(f"⚠️ Προσοχή: Η θέση είναι {qty} SOL. Θες να προχωρήσεις; (ναι/οχι): ")
        if confirm.lower() != "ναι":
            print("❌ Εντολή ακυρώθηκε.")
            return

    print(f"✅ Εκτελείται εντολή {side.upper()} {qty} SOL στο {entry}")
    print(f"➡️ SL: {sl}, TP1: {signal['tp1']}, TP2: {signal['tp2']}, TP3: {signal['tp3']}, TP4: {signal['tp4']}")

    # PLACE ORDER HERE (e.g., with requests.post to Bybit API)
    # For now just simulate:
    print("🧪 [Simulated] Order placed.")

# === RUN ===
if __name__ == "__main__":
    print("🚀 Bot έτοιμο! Περιμένει σήμα...")

    # TEMP: Χειροκίνητο test
    place_order(example_signal)

    # TODO: Σύνδεση με webhook_server + live signal parsing

