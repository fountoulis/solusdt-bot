# ✅ SOLUSDT Bot Logic - main.py (με ενσωματωμένο Trailing SL σε TP3/TP4)

from math import copysign

class TradeManager:
    def __init__(self, entry, sl, position_size, direction, atr):
        self.entry = entry
        self.sl = sl
        self.position_size = position_size
        self.direction = direction  # 'long' ή 'short'
        self.atr = atr
        self.r = abs(entry - sl)

        # TP targets (RR-based)
        self.tp1 = self._rr_target(2.5)
        self.tp2 = self._rr_target(3.0)
        self.tp3 = self._rr_target(3.5)
        self.tp4 = self._rr_target(4.0)

        self.tp_hit = [False, False, False, False]
        self.trailing_active = False
        self.trailing_sl = None
        self.last_trailing_price = None
        self.trailing_step = 0.5 * self.r  # changeable

    def _rr_target(self, rr):
        return self.entry + copysign(rr * self.r, 1 if self.direction == 'long' else -1)

    def update_price(self, current_price):
        # TP Check
        if not self.tp_hit[0] and self._tp_reached(current_price, self.tp1):
            self.tp_hit[0] = True
            self._log_tp(1)
        elif not self.tp_hit[1] and self._tp_reached(current_price, self.tp2):
            self.tp_hit[1] = True
            self._log_tp(2)
            self.trailing_active = True
            self.trailing_sl = self.entry  # break-even
            self.last_trailing_price = current_price
        elif not self.tp_hit[2] and self._tp_reached(current_price, self.tp3):
            self.tp_hit[2] = True
            self._log_tp(3)
        elif not self.tp_hit[3] and self._tp_reached(current_price, self.tp4):
            self.tp_hit[3] = True
            self._log_tp(4)

        # Trailing SL Update
        if self.trailing_active:
            progress = abs(current_price - self.last_trailing_price)
            if progress >= self.trailing_step:
                move = copysign(self.trailing_step, 1 if self.direction == 'long' else -1)
                self.trailing_sl += move
                self.last_trailing_price = current_price
                print(f"🔄 Trailing SL moved to {self.trailing_sl:.2f}")

        # Force SL Trigger Check
        if self.trailing_active:
            if (self.direction == 'long' and current_price <= self.trailing_sl) or \
               (self.direction == 'short' and current_price >= self.trailing_sl):
                print(f"❌ Trailing SL hit at {current_price:.2f}! Closing position...")
                return 'exit'

        return 'hold'

    def _tp_reached(self, price, target):
        return price >= target if self.direction == 'long' else price <= target

    def _log_tp(self, tp_number):
        print(f"✅ TP{tp_number} reached at price {getattr(self, f'tp{tp_number}'):.2f}")


# ✅ ΣΥΝΕΧΕΙΑ ΕΝΣΩΜΑΤΩΣΗΣ: webhook logic για να τροφοδοτεί το TradeManager με δεδομένα
# Θα χρειαστεί Flask route που δέχεται JSON από TradingView και δημιουργεί TradeManager instance

from flask import Flask, request, jsonify

app = Flask(__name__)
trade_manager = None

@app.route('/webhook', methods=['POST'])
def webhook():
    global trade_manager
    data = request.get_json()
    print("✅ RECEIVED DATA:", data)

    try:
        entry = float(data['entry'])
        sl = float(data['sl'])
        position_size = 100  # μπορεί να υπολογιστεί με risk mgmt logic
        direction = data['signal']  # 'long' ή 'short'
        atr = float(data['atr'])

        trade_manager = TradeManager(entry, sl, position_size, direction, atr)
        print("📥 TradeManager initialized with:", trade_manager.__dict__)
        return jsonify({"status": "TradeManager initialized"}), 200
    except Exception as e:
        print("❌ Error in webhook:", str(e))
        return jsonify({"error": str(e)}), 400

@app.route('/price_update', methods=['POST'])
def price_update():
    global trade_manager
    data = request.get_json()
    price = float(data['price'])

    if trade_manager is None:
        return jsonify({"status": "No trade active"}), 400

    status = trade_manager.update_price(price)
    return jsonify({"status": status}), 200

if __name__ == '__main__':
    print("🚀 Starting SOLUSDT bot on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
