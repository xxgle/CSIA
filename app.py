import os
from datetime import timedelta
from flask import Flask, redirect, url_for
from models import db

def create_app(): 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workoutgenerator.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    app.config['SESSION_COOKIE_HTTPONLY'] = True 
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) #sessions last for 7 days of inactivity

    db.init_app(app)

    from routes.auth import auth_bp

    app.register_blueprint(auth_bp) #makes the blueprints for auths

    @app.route('/') #the home page
    def index():
        return redirect(url_for('auth.dashboard'))

    with app.app_context(): #creates the tables
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
