from collections import Counter

from models.trade import Trade


def calculate_dashboard_stats(user_id):

    trades = Trade.query.filter_by(user_id=user_id).all()

    total = len(trades)

    wins = 0
    losses = 0

    symbols = Counter()

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

        "common_mistake": common_mistake

    }