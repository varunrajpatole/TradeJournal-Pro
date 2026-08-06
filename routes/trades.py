from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import db
from models.trade import Trade

trades_bp = Blueprint("trades", __name__)


# -----------------------------
# Add Trade
# -----------------------------
@trades_bp.route("/add_trade", methods=["GET", "POST"])
@login_required
def add_trade():

    if request.method == "POST":

        trade = Trade(
    date=request.form["date"],
    symbol=request.form["symbol"],
    direction=request.form["direction"],
    entry=float(request.form["entry"]),
    exit=float(request.form["exit"]),
    lot=float(request.form["lot"]),
    market=request.form["market"],

    strategy=request.form["strategy"],
    session=request.form["session"],
    emotion=request.form["emotion"],
    mistake=request.form["mistake"],

    notes=request.form["notes"],

    user_id=current_user.id
)

        db.session.add(trade)
        db.session.commit()

        return redirect(url_for("trades.trade_list"))

    return render_template("add_trade.html")


# -----------------------------
# View Trades
# -----------------------------
@trades_bp.route("/trades")
@login_required
def trade_list():

    trades = Trade.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "trades.html",
        trades=trades
    )


# -----------------------------
# Edit Trade
# -----------------------------
@trades_bp.route("/edit_trade/<int:id>", methods=["GET", "POST"])
@login_required
def edit_trade(id):

    trade = Trade.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        trade.date = request.form["date"]
        trade.symbol = request.form["symbol"]
        trade.direction = request.form["direction"]
        trade.entry = float(request.form["entry"])
        trade.exit = float(request.form["exit"])
        trade.lot = float(request.form["lot"])
        trade.market = request.form["market"]
        

        trade.strategy = request.form["strategy"]
        trade.session = request.form["session"]
        trade.emotion = request.form["emotion"]
        trade.mistake = request.form["mistake"]

        trade.notes = request.form["notes"]

        db.session.commit()

        return redirect(url_for("trades.trade_list"))

    return render_template(
        "edit_trade.html",
        trade=trade
    )


# -----------------------------
# Delete Trade
# -----------------------------
@trades_bp.route("/delete_trade/<int:id>")
@login_required
def delete_trade(id):

    trade = Trade.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(trade)
    db.session.commit()

    return redirect(url_for("trades.trade_list"))