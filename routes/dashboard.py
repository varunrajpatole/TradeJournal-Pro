from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
from models.trade import Trade

from analytics.stats import calculate_dashboard_stats
import calendar
from collections import defaultdict

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    stats = calculate_dashboard_stats(current_user.id)

    return render_template(
        "dashboard.html",
        user=current_user,
        **stats
    )
    
@dashboard_bp.route("/analytics")
@login_required
def analytics():

    stats = calculate_dashboard_stats(current_user.id)

    return render_template(
        "analytics.html",
        **stats
    )
    
@dashboard_bp.route("/calendar")
@login_required
def calendar_view():

    year = 2026
    month = 8

    cal = calendar.monthcalendar(year, month)

    trades = Trade.query.filter_by(user_id=current_user.id).all()
    trades_by_day = {}
    daily_profit = {}

    for trade in trades:

        try:

            trade_date = datetime.strptime(
                trade.date,
                "%Y-%m-%d"
            )

        except:

            continue

        if trade_date.year == year and trade_date.month == month:

            day = trade_date.day

            daily_profit[day] = daily_profit.get(day, 0) + (
                trade.profit_loss or 0
            )
            if day not in trades_by_day:
                trades_by_day[day] = []

            trades_by_day[day].append({
                "symbol": trade.symbol,
                "direction": trade.direction,
                "profit": trade.profit_loss
            })

    return render_template(
        "calendar.html",
        calendar_data=cal,
        month_name=calendar.month_name[month],
        year=year,
        daily_profit=daily_profit
        trades_by_day=trades_by_day,
    )
    
