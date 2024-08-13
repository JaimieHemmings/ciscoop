from flask import render_template, request, redirect, url_for, flash, session
from ciscoop import app, db
from ciscoop.models import User, Post, Message, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import Pagination
import re


@app.route('/')
@app.route('/index')
def home():
    """
    Index page
    This is the main page of the website.
    It displays the 3 most recent blog posts.
    The posts are ordered by the date they were created in descending order.
    """
    latest_posts = Post.query.order_by(Post.created.desc()).limit(3).all()
    return render_template('index.html', title="Home", posts=latest_posts)


@app.route('/blog')
def blog():
    """
    Blog page
    Implement SQLAlchemy pagination for Blog Page
    Then get the current page of posts and then the prev/next URLs
    """
    page = request.args.get('page', 1, type=int)
    curr_posts = Post.query.order_by(
        Post.created.desc()).paginate(page=page, per_page=5)
    next_url = url_for(
        'blog', page=curr_posts.next_num) if curr_posts.has_next else None
    prev_url = url_for(
        'blog', page=curr_posts.prev_num) if curr_posts.has_prev else None
    return render_template(
        'blog.html', title="Blog",
        posts=curr_posts.items,
        next_url=next_url,
        prev_url=prev_url)


@app.route('/blog/<slug>', methods=['GET', 'POST'])
def blog_post(slug):
    """
    Individual Blog post
    Check if the requested post exists and if not return a 404 error.
    """

    post = Post.query.filter_by(slug=slug).first()
    if post is None:
        return render_template('404.html', title="Uh oh! Error: 404"), 404

    """
    Get the form data in the case a user is returned to this page after
    submitting a comment that didn't pass validation
    """
    if request.method == 'POST':
        # Ensure user is logged in before commenting

        if 'user_id' not in session:
            flash("Please login to comment on this post.")
            return redirect(url_for('login'))
        submitted_comment = request.form.get('comment')
        username = session.get('username')
        user_id = session.get('user_id')

        # Validate the comment
        if len(submitted_comment) < 5 or len(submitted_comment) > 200:
            flash(
                "Comment must be greater than 5 characters"
                " and less than 200 characters.")
            return redirect(url_for(
                'blog_post',
                slug=slug,
                submitted_comment=submitted_comment)
            )

        # Create new comment
        new_comment = Comment(
            content=submitted_comment,
            post_id=post.id,
            user_id=user_id,
            username=username)

        # Add new comment to database
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!")
        return redirect(url_for('blog_post', slug=slug))

    # Get all comments for the post
    comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template(
        'blog-post.html',
        title=f"Blog Post - {post.title}",
        post=post,
        comments=comments,
        user_id=session.get('user_id'),
        submitted_comment=request.args.get('submitted_comment')
    )


# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # If the user is logged in set the form email value to the user's email
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        user_email = user.email
        if user.first_name and user.last_name:
            full_name = user.first_name + " " + user.last_name
        else:
            full_name = None
    else:
        full_name = None
        user_email = None
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
        'contact.html',
        title="Contact",
        user_email=user_email,
        full_name=full_name)


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
        # Ensure email address is not already used
        email_check = User.query.filter_by(email=email).first()
        if email_check:
            flash("Email address already in use. Please try again.")
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


# Edit Profile Page
@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please login to view your profile.")
        return redirect(url_for('login'))
    # Get user session
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        # get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        # Validate form data
        if len(first_name) < 2:
            flash("Your first name is too short to be valid.")
            return redirect(url_for('edit_profile'))
        if len(last_name) < 2:
            flash("Your last name is too short to be valid.")
            return redirect(url_for('edit_profile'))
        if len(email) < 5:
            flash("Your email is too short to be valid.")
            return redirect(url_for('edit_profile'))
        # update user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        # commit changes
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for('profile'))
    return render_template(
        'edit-profile.html', title="Edit Profile", user=user)


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
    if post is None:
        post = ""
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
    if len(messageData) == 0:
        messageData = ""
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


"""
    ----- Error Handling -----
    The below statements should catch and gracefully handle the majority,
    if not all, of the errors that could occur

"""


# Handle Bad Requests
@app.errorhandler(400)
def bad_request(e):
    return render_template(
        '400.html',
        title="Uh oh! Error: 400",
        error_message=e), 400


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html',
        title="Uh oh! Error: 404",
        error_message=e), 404


# Handle Timeout Errors
@app.errorhandler(408)
def request_timeout(e):
    return render_template(
        '408.html',
        title="Uh oh! Error: 408",
        error_message=e), 408


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        '500.html',
        title="Uh oh! Error: 500",
        error_message=e), 500
