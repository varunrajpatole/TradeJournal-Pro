from collections import Counter

from models.trade import Trade


def calculate_dashboard_stats(user_id):

    trades = Trade.query.filter_by(user_id=user_id).all()

    total = len(trades)

    wins = 0
    losses = 0

    symbols = Counter()
    market_counter = Counter()

    strategy_stats = {}

    session_stats = {}

    losing_emotions = []

    mistakes = []

    for trade in trades:

        # Winner / Loser

        if trade.direction == "BUY":
            is_win = trade.exit > trade.entry
        else:
            is_win = trade.exit < trade.entry

        if is_win:
            wins += 1
        else:
            losses += 1

        # Pair

        symbols[trade.symbol] += 1
        market = trade.market or "Unknown"

        market_counter[market] += 1

        # Strategy

        if trade.strategy not in strategy_stats:

            strategy_stats[trade.strategy] = {
                "wins": 0,
                "total": 0
            }

        strategy_stats[trade.strategy]["total"] += 1

        if is_win:
            strategy_stats[trade.strategy]["wins"] += 1

        # Session

        if trade.session not in session_stats:

            session_stats[trade.session] = {
                "wins": 0,
                "total": 0
            }

        session_stats[trade.session]["total"] += 1

        if is_win:
            session_stats[trade.session]["wins"] += 1

        # Emotion

        if not is_win and trade.emotion:

            losing_emotions.append(trade.emotion)

        # Mistake

        if trade.mistake and trade.mistake != "None":

            mistakes.append(trade.mistake)

    # -----------------------
    # -----------------------
# Financial Statistics
# -----------------------

    profits = [
    t.profit_loss
    for t in trades
    if t.profit_loss is not None and t.profit_loss > 0
    ]

    loss_values = [
        t.profit_loss
        for t in trades
        if t.profit_loss is not None and t.profit_loss < 0
    ]

    total_profit = round(
        sum(t.profit_loss or 0 for t in trades),
        2
    )
    
    average_win = round(sum(profits) / len(profits), 2) if profits else 0

    average_loss = round(sum(loss_values) / len(loss_values), 2) if loss_values else 0

    largest_win = round(max(profits), 2) if profits else 0

    largest_loss = round(min(loss_values), 2) if loss_values else 0
    
    win_rate = round((wins / total) * 100, 2) if total else 0

    most_traded = symbols.most_common(1)[0][0] if symbols else "-"

    # -----------------------
    # Best Strategy
    # -----------------------

    best_strategy = "-"

    best_strategy_rate = 0

    for strategy, data in strategy_stats.items():

        rate = (data["wins"] / data["total"]) * 100

        if rate > best_strategy_rate:

            best_strategy_rate = rate

            best_strategy = strategy

    # -----------------------
    # Best Session
    # -----------------------

    best_session = "-"

    best_session_rate = 0

    for session, data in session_stats.items():

        rate = (data["wins"] / data["total"]) * 100

        if rate > best_session_rate:

            best_session_rate = rate

            best_session = session

    # -----------------------

    common_emotion = "-"

    if losing_emotions:

        common_emotion = Counter(
            losing_emotions
        ).most_common(1)[0][0]

    common_mistake = "-"

    if mistakes:

        common_mistake = Counter(
            mistakes
        ).most_common(1)[0][0]
    # -----------------------
# Recent Trades
# -----------------------

    recent_trades = (
        Trade.query
        .filter_by(user_id=user_id)
        .order_by(Trade.id.desc())
        .limit(5)
        .all()
    )
    equity_curve = []
    equity_dates = []
    starting_balance = 10000   # Change later from Settings page

    balance = starting_balance

    all_trades = (
        Trade.query
        .filter_by(user_id=user_id)
        .order_by(Trade.id.asc())
        .all()
    )

    for trade in all_trades:

        balance += trade.profit_loss or 0

        equity_curve.append(round(balance,2))
        
        equity_dates.append(trade.date)
        
    current_equity = balance
    # -----------------------
# Strategy Chart Data
# -----------------------

    strategy_labels = []
    strategy_rates = []

    for strategy, data in strategy_stats.items():

        strategy_labels.append(strategy)

        rate = round(
            (data["wins"] / data["total"]) * 100,
            2
        )

        strategy_rates.append(rate)
    # -----------------------
    # Session Chart Data
    # -----------------------

    session_labels = []
    session_rates = []

    for session, data in session_stats.items():

        session_labels.append(session)

        rate = round(
            (data["wins"] / data["total"]) * 100,
            2
        )

        session_rates.append(rate)
        
    market_labels = list(market_counter.keys())
    market_counts = list(market_counter.values())
    emotion_counter = Counter(losing_emotions)

    emotion_labels = list(emotion_counter.keys())

    emotion_counts = list(emotion_counter.values())
    mistake_counter=Counter(mistakes)

    mistake_labels=list(mistake_counter.keys())

    mistake_counts=list(mistake_counter.values())
    return {

        "total": total,

        "wins": wins,

        "losses": losses,

        "win_rate": win_rate,

        "most_traded": most_traded,

        "best_strategy": best_strategy,

        "best_strategy_rate": round(best_strategy_rate, 2),

        "best_session": best_session,

        "best_session_rate": round(best_session_rate, 2),

        "common_emotion": common_emotion,

        "common_mistake": common_mistake,
        
        "total_profit": total_profit,

        "average_win": average_win,

        "average_loss": average_loss,

        "largest_win": largest_win,

        "largest_loss": largest_loss,
        
        "recent_trades": recent_trades,
        
        "pie_labels": ["Wins", "Losses"],
        "pie_data": [wins, losses],

        "strategy_labels": strategy_labels,
        "strategy_rates": strategy_rates,
        
        "session_labels": session_labels,
        "session_rates": session_rates,
        "market_labels": market_labels,
        "market_counts": market_counts,
        "emotion_labels":emotion_labels,

        "emotion_counts":emotion_counts,
        "mistake_labels":mistake_labels,

        "mistake_counts":mistake_counts,
        "equity_curve": equity_curve,
        "equity_dates": equity_dates,
        "current_equity": current_equity,
    }