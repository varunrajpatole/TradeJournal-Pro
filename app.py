from flask import send_from_directory
from flask_migrate import Migrate
from flask import Flask
from config import Config
from models import db, login_manager
from models.user import User
from routes.auth import auth
from routes.dashboard import dashboard_bp
from routes.trades import trades_bp

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(trades_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return """
    <h1>🚀 Trade Journal</h1>
    <h3>Backend is Working!</h3>
    """


with app.app_context():
    db.create_all()

from flask import send_from_directory

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=True)