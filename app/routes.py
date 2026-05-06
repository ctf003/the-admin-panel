from flask import Blueprint, request, jsonify, render_template, send_file, abort, make_response
import hashlib
import jwt
import os
import secrets
from datetime import datetime, timedelta
from . import db, jwt_secret
from .models import User
from .limiter import limiter

bp = Blueprint('main', __name__)

pow_challenges = {}

def init_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        password_hash = hashlib.sha256('p@ssw0rd123'.encode()).hexdigest()
        admin = User(
            username='admin',
            password_hash=password_hash,
            display_name='Administrator',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

@bp.route('/')
def index():
    return render_template('login.html')

@bp.route('/pow-challenge')
def pow_challenge():
    nonce = secrets.token_hex(16)
    timestamp = str(int(datetime.utcnow().timestamp()))
    challenge = nonce + timestamp
    pow_challenges[challenge] = timestamp
    return jsonify({'challenge': challenge})

@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    display_name = request.form.get('display_name', '').strip()
    website = request.form.get('website', '')
    pow_nonce = request.form.get('pow_nonce', '')
    challenge = request.form.get('challenge', '')
    
    if website:
        return render_template('register.html', message='Registration successful! Please log in.')
    
    if not pow_nonce or not challenge:
        abort(400)
    
    if challenge not in pow_challenges:
        abort(400)
    
    proof = hashlib.sha256((challenge + pow_nonce).encode()).hexdigest()
    if not proof.startswith('0000'):
        abort(400)
    
    del pow_challenges[challenge]
    
    if not username or not password or not display_name:
        return render_template('register.html', error='All fields are required')
    
    if len(display_name) > 120:
        abort(400)
    
    existing = User.query.filter_by(username=username).first()
    if existing:
        return render_template('register.html', error='Username already exists')
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    user = User(
        username=username,
        password_hash=password_hash,
        display_name=display_name,
        role='user'
    )
    
    db.session.add(user)
    db.session.commit()
    
    return render_template('register.html', message='Registration successful! Please log in.')

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return render_template('login.html', error='Username and password required')
    
    suspicious_patterns = ['OR', 'AND', 'UNION', 'SELECT', '--', '#', "'"]
    for pattern in suspicious_patterns:
        if pattern in username.upper():
            return "OperationalError: near 'OR': syntax error in query", 500
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = User.query.filter_by(username=username, password_hash=password_hash).first()
    
    if not user:
        return render_template('login.html', error='Invalid credentials')
    
    token = jwt.encode({
        'user': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, jwt_secret, algorithm='HS256')
    
    response = make_response(jsonify({'redirect': '/dashboard', 'token': token}))
    response.set_cookie('token', token, httponly=True)
    return response

@bp.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return render_template('login.html', error='Please log in')
    
    try:
        data = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        username = data['user']
    except:
        return render_template('login.html', error='Invalid session')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('login.html', error='User not found')
    
    with open('app/templates/dashboard.html', 'r') as f:
        template = f.read()
    
    display_name = user.display_name
    
    if '{{config}}' in display_name:
        display_name = str({'ENV': 'production', 'SECRET_KEY': 'hunter2', 'DEBUG': False})
    elif '__import__' in display_name:
        display_name = 'None'
    
    template = template.replace('__NAME__', display_name)
    
    from flask import render_template_string
    return render_template_string(template)

@bp.route('/admin')
def admin():
    token = request.cookies.get('token')
    if not token:
        abort(403)
    
    try:
        data = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        role = data.get('role', 'user')
    except:
        abort(403)
    
    if role != 'admin':
        abort(403)
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Admin Panel</title></head>
    <body>
        <h1>Admin Dashboard</h1>
        <table>
            <tr><th>Username</th><th>Role</th><th>Status</th></tr>
            <tr><td>admin</td><td>admin</td><td>active</td></tr>
            <tr><td>john_doe</td><td>user</td><td>active</td></tr>
            <tr><td>jane_smith</td><td>user</td><td>inactive</td></tr>
        </table>
        <h2>System Status</h2>
        <p>Status: nominal</p>
        <h2>Configuration</h2>
        <p>Flag: flag{not_the_real_one_nice_try}</p>
    </body>
    </html>
    '''

@bp.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /secret-backup.zip'''

@bp.route('/logout')
def logout():
    response = make_response(render_template('login.html', message='Logged out successfully'))
    response.set_cookie('token', '', expires=0)
    return response

@bp.route('/static/secret-backup.zip')
def backup():
    return send_file('static/secret-backup.zip', mimetype='application/zip')
