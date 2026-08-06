from models import db

class Trade(db.Model):

    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(50))

    symbol = db.Column(db.String(20))

    direction = db.Column(db.String(10))

    entry = db.Column(db.Float)

    exit = db.Column(db.Float)

    lot = db.Column(db.Float)

    profit = db.Column(db.Float)

    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))