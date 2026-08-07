from flask import Blueprint, render_template
from flask_login import login_required, current_user

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

    return render_template("calendar.html")
    
