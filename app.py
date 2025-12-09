"""
Climate Change Community Platform
A safe, calm, and inclusive space for sharing experiences and knowledge about climate change.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE'] = 'climate_community.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database initialization
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_moderator INTEGER DEFAULT 0
    )''')
    
    # Posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Comments table
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Reactions table (likes/support)
    c.execute('''CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        reaction_type TEXT DEFAULT 'like',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE(post_id, user_id)
    )''')
    
    # Reports table
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        comment_id INTEGER,
        reporter_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (comment_id) REFERENCES comments(id),
        FOREIGN KEY (reporter_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html')
        
        conn = get_db()
        c = conn.cursor()
        
        # Check if username or email already exists
        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            flash('Username or email already exists.', 'error')
            conn.close()
            return render_template('signup.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                  (username, email, password_hash))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        conn = get_db()
        c = conn.cursor()
        user = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_moderator'] = user['is_moderator']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('forum'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forum')
def forum():
    """Forum main page with posts"""
    category = request.args.get('category', 'all')
    conn = get_db()
    c = conn.cursor()
    
    if category == 'all':
        posts = c.execute('''
            SELECT p.*, u.username, COUNT(DISTINCT r.id) as reaction_count, COUNT(DISTINCT c.id) as comment_count
            FROM posts p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN reactions r ON p.id = r.post_id
            LEFT JOIN comments c ON p.id = c.post_id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        ''').fetchall()
    else:
        posts = c.execute('''
            SELECT p.*, u.username, COUNT(DISTINCT r.id) as reaction_count, COUNT(DISTINCT c.id) as comment_count
            FROM posts p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN reactions r ON p.id = r.post_id
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.category = ?
            GROUP BY p.id
            ORDER BY p.created_at DESC
        ''', (category,)).fetchall()
    
    conn.close()
    
    categories = [
        'Heatwaves',
        'Flooding',
        'Strong winds & storms',
        'Emotional & mental health impacts',
        'Daily life experiences'
    ]
    
    return render_template('forum.html', posts=posts, categories=categories, current_category=category)

@app.route('/forum/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new forum post"""
    if request.method == 'POST':
        category = request.form.get('category')
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not category or not title or not content:
            flash('All fields are required.', 'error')
            return render_template('create_post.html')
        
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO posts (user_id, category, title, content) VALUES (?, ?, ?, ?)',
                  (session['user_id'], category, title, content))
        conn.commit()
        conn.close()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('forum'))
    
    categories = [
        'Heatwaves',
        'Flooding',
        'Strong winds & storms',
        'Emotional & mental health impacts',
        'Daily life experiences'
    ]
    return render_template('create_post.html', categories=categories)

@app.route('/forum/post/<int:post_id>')
def view_post(post_id):
    """View a single post with comments"""
    conn = get_db()
    c = conn.cursor()
    
    post = c.execute('''
        SELECT p.*, u.username, COUNT(DISTINCT r.id) as reaction_count
        FROM posts p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN reactions r ON p.id = r.post_id
        WHERE p.id = ?
        GROUP BY p.id
    ''', (post_id,)).fetchone()
    
    if not post:
        flash('Post not found.', 'error')
        conn.close()
        return redirect(url_for('forum'))
    
    comments = c.execute('''
        SELECT c.*, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    ''', (post_id,)).fetchall()
    
    # Check if user has reacted
    user_reacted = False
    if 'user_id' in session:
        reaction = c.execute('SELECT id FROM reactions WHERE post_id = ? AND user_id = ?',
                           (post_id, session['user_id'])).fetchone()
        user_reacted = reaction is not None
    
    conn.close()
    
    return render_template('view_post.html', post=post, comments=comments, user_reacted=user_reacted)

@app.route('/forum/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a post"""
    content = request.form.get('content')
    
    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('view_post', post_id=post_id))
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)',
              (post_id, session['user_id'], content))
    conn.commit()
    conn.close()
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/forum/post/<int:post_id>/react', methods=['POST'])
@login_required
def react_to_post(post_id):
    """Add or remove reaction to a post"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if user already reacted
    existing = c.execute('SELECT id FROM reactions WHERE post_id = ? AND user_id = ?',
                        (post_id, session['user_id'])).fetchone()
    
    if existing:
        # Remove reaction
        c.execute('DELETE FROM reactions WHERE post_id = ? AND user_id = ?',
                 (post_id, session['user_id']))
        action = 'removed'
    else:
        # Add reaction
        c.execute('INSERT INTO reactions (post_id, user_id, reaction_type) VALUES (?, ?, ?)',
                 (post_id, session['user_id'], 'like'))
        action = 'added'
    
    conn.commit()
    
    # Get updated reaction count
    count = c.execute('SELECT COUNT(*) as count FROM reactions WHERE post_id = ?', (post_id,)).fetchone()['count']
    conn.close()
    
    return jsonify({'success': True, 'action': action, 'count': count})

@app.route('/forum/post/<int:post_id>/report', methods=['POST'])
@login_required
def report_post(post_id):
    """Report a post"""
    reason = request.form.get('reason')
    description = request.form.get('description', '')
    
    if not reason:
        flash('Please select a reason for reporting.', 'error')
        return redirect(url_for('view_post', post_id=post_id))
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO reports (post_id, reporter_id, reason, description) VALUES (?, ?, ?, ?)',
              (post_id, session['user_id'], reason, description))
    conn.commit()
    conn.close()
    
    flash('Thank you for reporting. Our moderators will review this content.', 'success')
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/seville')
def seville():
    """Seville climate change impacts page"""
    return render_template('seville.html')

@app.route('/learn')
def learn():
    """Learn page with climate resources"""
    return render_template('learn.html')

@app.route('/guidelines')
def guidelines():
    """Community guidelines page"""
    return render_template('guidelines.html')

@app.route('/healing-earth')
def healing_earth():
    """Healing Earth inspired section"""
    return render_template('healing_earth.html')

# Initialize database on first run
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

