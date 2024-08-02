from flask import render_template, request, redirect, url_for, flash, session
from ciscoop import app, db
from ciscoop.models import User, Post, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import Pagination
import re


# Index page
@app.route('/')
@app.route('/index')
def home():
    # Get 3 latest blog posts
    latest_posts = Post.query.order_by(Post.created.desc()).limit(3).all()
    return render_template('index.html', title="Home", posts=latest_posts)


# Blog page
@app.route('/blog')
def blog():
    # Implement SQLAlchemy pagination for Blog Page
    page = request.args.get('page', 1, type=int)
    # Get current page of posts
    curr_posts = Post.query.order_by(
        Post.created.desc()).paginate(page=page, per_page=5)
    # Get next and previous page URLs
    next_url = url_for(
        'blog', page=curr_posts.next_num) if curr_posts.has_next else None
    prev_url = url_for(
        'blog', page=curr_posts.prev_num) if curr_posts.has_prev else None
    return render_template(
        'blog.html', title="Blog",
        posts=curr_posts.items,
        next_url=next_url,
        prev_url=prev_url)


# Individual Blog Posts
@app.route('/blog/<slug>')
def blog_post(slug):
    # Get post by slug
    post = Post.query.filter_by(slug=slug).first()
    # Check if post exists
    if post is None:
        # Return 404 page
        return render_template('404.html', title="Uh oh! Error: 404"), 404
    return render_template('blog-post.html', title="Blog Post", post=post)


# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # If the user is logged in set the form email value to the user's email
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        user_email = user.email
    if request.method == 'POST':
        # get form data
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        message = request.form['message']
        # Validate Form Data
        if len(name) < 2:
            flash("Your name is too short to be valid.")
            return redirect(url_for('contact'))
        if len(email) < 5:
            flash("Your email is too short to be valid.")
            return redirect(url_for('contact'))
        else:
            if not re.match(regex, email):
                flash("Invalid email address. Please try again.")
                return redirect(url_for('contact'))
        if len(title) < 3:
            flash("The title must be longer than 3 characters.")
            return redirect(url_for('contact'))
        if len(message) < 5 or len(message) > 280:
            flash(
                "Message must be greater than 5 "
                "characters and less than 280 characters.")
            return redirect(url_for('contact'))
        # create new message
        new_message = Message(
            name=name, email=email, content=message, title=title)
        # add new message to database
        db.session.add(new_message)
        db.session.commit()
        flash("Message sent successfully!")
        return redirect(url_for('contact'))
    return render_template(
        'contact.html', title="Contact", user_email=user_email)


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']
        # Check if user exists
        user = User.query.filter_by(username=username).first()
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
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists. Please try again.")
            return redirect(url_for('register'))
        # Check the password confirmation matches
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))
        # create new user
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            role="user")
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
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html', title="Profile", user=user)


# Admin Page
@app.route('/profile/admin', methods=['GET', 'POST'])
def admin():
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Get user session
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        # Check user is an admin
        if user.role != "admin":
            flash("You do not have permission to access this page.")
            return redirect(url_for('home'))
        # get form data
        title = request.form['title']
        content = request.form.get('ckeditor')
        slug = title.lower().replace(" ", "-")
        preview = request.form['preview']
        # Validate data from form
        if len(title) < 3:
            flash("Please create a more descriptive title")
            return redirect(url_for('admin'))
        if len(content) < 100:
            flash("A blog post needs to be longer than 100 characters")
            return redirect(url_for('admin'))
        if len(preview) < 5:
            flash("Please create a more descriptive preview string")
            return redirect(url_for('admin'))
        # create new post
        new_post = Post(
            title=title,
            content=content,
            preview=preview,
            user_id=user_id,
            slug=slug,
            user=user)
        # add new post to database
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!")
        return redirect(url_for('admin'))
    # Get all blog posts
    all_posts = Post.query.all()
    messageData = Message.query.all()
    newMessages = len(messageData)
    return render_template(
        'admin.html',
        title="Admin",
        posts=all_posts,
        newMessages=newMessages)


# Edit posts list
@app.route('/profile/admin/edit-posts/', methods=['GET', 'POST'])
def posts_list():
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Implement SQLAlchemy pagination for Blog Page
    page = request.args.get('page', 1, type=int)
    # Get current page of posts
    curr_posts = Post.query.order_by(
        Post.created.desc()).paginate(page=page, per_page=5)
    # Get next and previous page URLs
    next_url = url_for(
        'posts_list',
        page=curr_posts.next_num
        ) if curr_posts.has_next else None
    prev_url = url_for(
        'posts_list',
        page=curr_posts.prev_num
        ) if curr_posts.has_prev else None
    return render_template(
        'posts-list.html',
        title="Edit Posts",
        posts=curr_posts.items,
        next_url=next_url,
        prev_url=prev_url)


# Edit Post
@app.route('/profile/admin/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get post by id
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        # get form data
        title = request.form['title']
        content = request.form.get('ckeditor')
        slug = title.lower().replace(" ", "-")
        preview = request.form['preview']
        # update post
        post.title = title
        post.preview = preview
        post.content = content
        post.slug = slug
        # commit changes
        db.session.commit()
        flash("Post updated successfully!")
        return redirect(url_for('posts_list'))
    return render_template('edit-post.html', title="Edit Post", post=post)


# Delete Post
@app.route('/profile/admin/delete-post/<int:id>')
def delete_post(id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get post by id
    post = Post.query.filter_by(id=id).first()
    # Delete post
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!")
    return redirect(url_for('posts_list'))


# Messages Page
@app.route('/admin/messages', methods=['GET', 'POST'])
def messages_page():
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get all messages
    messageData = Message.query.all()
    return render_template(
        'messages.html',
        title="Messages",
        messages=messageData)


# Delete Message
@app.route('/admin/messages/delete/<int:id>')
def delete_message(id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    # Check user is an admin
    if user.role != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    # Get message by id
    message = Message.query.filter_by(id=id).first()
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
    return render_template(
        '404.html',
        title="Uh oh! Error: 404",
        error_message=e), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        '500.html',
        title="Uh oh! Error: 500",
        error_message=e), 500
