from flask import render_template, request, redirect, url_for, flash, session
from ciscoop import app, db
from ciscoop.models import users, posts, messages
from werkzeug.security import generate_password_hash, check_password_hash

# Index page
@app.route('/')
def home():
    # Get 3 latest blog posts
    latest_posts = posts.query.order_by(posts.created.desc()).limit(3).all()
    return render_template('index.html', title = "Home", posts = latest_posts)

# Blog page
@app.route('/blog')
def blog():
    # Get all blog posts in ascending order
    all_posts = posts.query.order_by(posts.created.asc()).all()
    return render_template('blog.html', title="Blog", posts=all_posts)

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # get form data
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        message = request.form['message']
        # create new message
        new_message = messages(name=name, email=email, content=message, title=title)
        # add new message to database
        db.session.add(new_message)
        db.session.commit()
        flash("Message sent successfully!")
        return redirect(url_for('contact'))
    return render_template('contact.html', title="Contact")

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']
        # Check if user exists
        user = users.query.filter_by(username=username).first()
        # Check if password matches
        if user and check_password_hash(user.password, password):
            # Create session with user id
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f"Login successful! Welcome {user.username}.")
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password. Please try again.")
            return redirect(url_for('login'))
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

# Profile page
@app.route('/profile')
def profile():
    # Get user session
    user_id = session['user_id']
    user = users.query.filter_by(id=user_id).first()
    return render_template('profile.html', title="Profile", user=user)

# Admin Page
@app.route('/profile/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get user session
        user_id = session['user_id']
        # Check user is logged in
        if user_id is None:
            flash("Please login to create a post.")
            return redirect(url_for('login'))
        user = users.query.filter_by(id=user_id).first()
        # Check user is an admin
        if user.role != "admin":
            flash("You do not have permission to access this page.")
            return redirect(url_for('home'))
        # get form data
        title = request.form['title']
        content = request.form['content']
        slug = title.lower().replace(" ", "-")
        # create new post
        new_post = posts(title=title, content=content, user_id=user_id, slug=slug, user=user)
        # add new post to database
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!")
        return redirect(url_for('admin'))
    # Get all blog posts
    all_posts = posts.query.all()
    
    messageData = messages.query.all()
    newMessages = len(messageData)

    return render_template('admin.html', title="Admin", posts=all_posts, newMessages = newMessages)

# Messages Page
@app.route('/admin/messages', methods=['GET', 'POST'])
def messages_page():
    # Get user session
    user_id = session['user_id']
    # Check user is logged in
    if user_id is None:
        flash("Please login to view messages.")
        return redirect(url_for('login'))
    user = users.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get all messages
    messageData = messages.query.all()
    return render_template('messages.html', title="Messages", messages=messageData)

# Delete Message
@app.route('/admin/messages/delete/<int:id>')
def delete_message(id):
    # Get user session
    user_id = session['user_id']
    # Check user is logged in
    if user_id is None:
        flash("Please login to delete a message.")
        return redirect(url_for('login'))
    user = users.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get message by id
    message = messages.query.filter_by(id=id).first()
    # Delete message
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully!")
    return redirect(url_for('messages_page'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('home'))

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Uh oh! Error: 404"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Uh oh! Error: 500"), 500