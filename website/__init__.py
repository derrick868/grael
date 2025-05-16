from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Use PostgreSQL if DATABASE_URL is set, fallback to SQLite
    db_url = os.getenv('DATABASE_URL', f"sqlite:///database.sqlite3")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CSRFProtect(app)
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer,Category

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    @app.context_processor
    def inject_categories():
        categories = Category.query.all()
        return dict(categories=categories)

    with app.app_context():
        db.create_all()  # Only useful if tables don't exist

    return app
