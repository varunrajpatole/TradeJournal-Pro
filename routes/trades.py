from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db
from models.trade import Trade
import os
import uuid

trades_bp = Blueprint("trades", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(file, prefix):
    """
    Save uploaded image with a unique filename.
    Returns filename or None.
    """

    if not file or file.filename == "":
        return None

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}_{prefix}{ext}"

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return filename


# ==========================================================
# ADD TRADE
# ==========================================================

@trades_bp.route("/add_trade", methods=["GET", "POST"])
@login_required
def add_trade():

    if request.method == "POST":

        before_image = save_uploaded_file(
            request.files.get("before_image"),
            "before"
        )

        after_image = save_uploaded_file(
            request.files.get("after_image"),
            "after"
        )

        trade = Trade(

            date=request.form["date"],

            symbol=request.form["symbol"],

            direction=request.form["direction"],

            entry=float(request.form["entry"]),

            exit=float(request.form["exit"]),

            lot=float(request.form["lot"]),

            market=request.form["market"],

            profit_loss=float(
                request.form.get("profit_loss") or 0
            ),

            commission=float(
                request.form.get("commission") or 0
            ),

            risk=float(
                request.form.get("risk") or 0
            ),

            strategy=request.form["strategy"],

            session=request.form["session"],

            emotion=request.form["emotion"],

            mistake=request.form["mistake"],

            notes=request.form["notes"],

            before_image=before_image,

            after_image=after_image,

            user_id=current_user.id

        )

        db.session.add(trade)
        db.session.commit()

        return redirect(url_for("trades.trade_list"))

    return render_template("add_trade.html")


# ==========================================================
# TRADE DETAILS
# ==========================================================

@trades_bp.route("/trade/<int:trade_id>")
@login_required
def trade_details(trade_id):

    trade = Trade.query.filter_by(
        id=trade_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "trade_details.html",
        trade=trade
    )


# ==========================================================
# TRADE LIST
# ==========================================================

@trades_bp.route("/trades")
@login_required
def trade_list():

    query = Trade.query.filter_by(user_id=current_user.id)

    # -----------------------
    # Filters
    # -----------------------

    symbol = request.args.get("symbol")
    market = request.args.get("market")
    strategy = request.args.get("strategy")
    session = request.args.get("session")

    if symbol:
        query = query.filter_by(symbol=symbol)

    if market:
        query = query.filter_by(market=market)

    if strategy:
        query = query.filter_by(strategy=strategy)

    if session:
        query = query.filter_by(session=session)

    page = request.args.get("page", 1, type=int)

    pagination = (
        query
        .order_by(Trade.date.desc())
        .paginate(page=page, per_page=10)
    )

    trades = pagination.items

    return render_template(
    "trades.html",
    trades=trades,
    pagination=pagination
    )   
# ==========================================================
# EDIT TRADE
# ==========================================================

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

        trade.profit_loss = float(
            request.form.get("profit_loss") or 0
        )

        trade.commission = float(
            request.form.get("commission") or 0
        )

        trade.risk = float(
            request.form.get("risk") or 0
        )

        trade.strategy = request.form["strategy"]
        trade.session = request.form["session"]
        trade.emotion = request.form["emotion"]
        trade.mistake = request.form["mistake"]

        trade.notes = request.form["notes"]

        # -------------------------
        # Replace images only if new
        # -------------------------

        before_image = save_uploaded_file(
            request.files.get("before_image"),
            "before"
        )

        if before_image:
            trade.before_image = before_image

        after_image = save_uploaded_file(
            request.files.get("after_image"),
            "after"
        )

        if after_image:
            trade.after_image = after_image

        db.session.commit()

        return redirect(url_for("trades.trade_list"))

    return render_template(
        "edit_trade.html",
        trade=trade
    )


# ==========================================================
# DELETE TRADE
# ==========================================================

@trades_bp.route("/delete_trade/<int:id>")
@login_required
def delete_trade(id):

    trade = Trade.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    # -------------------------
    # Delete uploaded images
    # -------------------------

    if trade.before_image:

        before_path = os.path.join(
            UPLOAD_FOLDER,
            trade.before_image
        )

        if os.path.exists(before_path):
            os.remove(before_path)

    if trade.after_image:

        after_path = os.path.join(
            UPLOAD_FOLDER,
            trade.after_image
        )

        if os.path.exists(after_path):
            os.remove(after_path)

    db.session.delete(trade)
    db.session.commit()

    return redirect(url_for("trades.trade_list"))