from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') #blueprint for the login and signup system. auth is the prefix


@auth_bp.route('/dashboard') #if the user is logged in they will be redirected to the dashboard. if not they go to login
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('auth/dashboard.html', user=user)


@auth_bp.route('/login', methods=['GET', 'POST']) #the login route
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')

        session.permanent = True
        session['user_id'] = user.id
        return redirect(url_for('auth.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/signup', methods=['GET', 'POST']) #the signup route
def signup():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard')) #if the user has an account redirects to the dashboard
        #username is restricted between 3 and 20 chars, password is between 6 and 72

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('auth/signup.html')

        if len(username) > 20:
            flash('Username must be 20 characters or fewer.', 'error')
            return render_template('auth/signup.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('auth/signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/signup.html')
        
        if len(password) > 72:
            flash('Password must be at most 72 characters.', 'error')
            return render_template('auth/signup.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return render_template('auth/signup.html')

        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        session.permanent = True
        session['user_id'] = user.id
        return redirect(url_for('auth.login')) #goes to login after making an account

    return render_template('auth/signup.html')


@auth_bp.route('/logout') #the logout route. clears the session and redirects to login
def logout():
    session.clear()
    return redirect(url_for('auth.login'))