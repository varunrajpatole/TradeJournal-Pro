from models import db

class Trade(db.Model):

    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(20), nullable=False)

    symbol = db.Column(db.String(20), nullable=False)

    direction = db.Column(db.String(10), nullable=False)

    entry = db.Column(db.Float, nullable=False)

    exit = db.Column(db.Float, nullable=False)

    lot = db.Column(db.Float, nullable=False)

    strategy = db.Column(db.String(50), default="")

    session = db.Column(db.String(30), default="")

    emotion = db.Column(db.String(50), default="")

    mistake = db.Column(db.String(100), default="")

    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))