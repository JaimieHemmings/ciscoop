from flask import render_template, request, redirect, url_for, flash
from ciscoop import app, db
from ciscoop.models import users, posts, messages
from werkzeug.security import generate_password_hash, check_password_hash

# Index page
@app.route('/')
def home():
    return render_template('index.html', title = "Home")

# Blog page
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', title="Blog")

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', title="Contact")

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="Login")

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        # Chek if user already exists
        user = users.query.filter_by(username=username).first()
        if user:
            flash("Username already exists. Please try again.")
            return redirect(url_for('register'))
        # Check the password confirmation matches
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))
        # create new user
        new_user = users(username=username, password=generate_password_hash(password), email=email, role="user")
        # add new user to database
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully! Please Login.")
        # redirect to login page
        return redirect(url_for('login'))
    return render_template('register.html', title="Register")

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Uh oh! Error: 404"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Uh oh! Error: 500"), 500