from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("trades.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    conn = get_db_connection()
    trades = conn.execute("SELECT * FROM trades").fetchall()

    total_trades = len(trades)
    winning_trades = len([t for t in trades if t["profit"] is not None and t["profit"] > 0])
    losing_trades = total_trades - winning_trades
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    profits = [t["profit"] for t in trades if t["profit"] is not None]

    conn.close()

    return render_template(
        "index.html",
        trades=trades,
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        win_rate=round(win_rate, 2),
        profits=profits
    )

# ---------------- ADD TRADE ----------------
@app.route("/add-trade", methods=["GET", "POST"])
def add_trade():
    if request.method == "POST":
        symbol = request.form["symbol"]
        trade_type = request.form["trade_type"]
        entry_price = float(request.form["entry_price"])
        exit_price = float(request.form["exit_price"])
        lot_size = float(request.form["lot_size"])
        strategy = request.form["strategy"]

        # ---- Pip Calculation ----
        if symbol == "XAUUSD":
            pips = (exit_price - entry_price) / 0.01
            pip_value = 1
        else:
            pips = (exit_price - entry_price) / 0.0001
            pip_value = 10

        if trade_type == "SELL":
            pips = -pips

        profit = pips * pip_value * lot_size

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO trades 
            (symbol, trade_type, entry_price, exit_price, lot_size, pips, strategy, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (symbol, trade_type, entry_price, exit_price, lot_size, round(pips,2), strategy, round(profit,2)))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_trade.html")

# ---------------- DELETE TRADE ----------------
@app.route("/delete-trade/<int:trade_id>")
def delete_trade(trade_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
