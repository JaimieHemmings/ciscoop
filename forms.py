
from flask_wtf import FlaskForm  # noqa
from wtforms import (
  StringField, PasswordField, EmailField, SubmitField, validators)
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


# Create a Form Class for Contact Page
class ContactForm(FlaskForm):

    name = StringField('Name', [validators.Length(
        min=5, max=50,
        message="Name must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Name"})

    email = EmailField('Email', [validators.Length(
        min=5, max=50,
        message="Email must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Email"})

    title = StringField('Title', [validators.Length(
        min=5, max=50,
        message="Title must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Message Title"})

    message = StringField('Message', [validators.Length(
        min=10, max=280,
        message="Message must be between 10 and 280 characters.")],
        widget=TextArea(),
        render_kw={"placeholder": "Your Message"})

    submit = SubmitField('Submit')


# Create a Form Class for Login Page
class LoginForm(FlaskForm):

    username = StringField('Username', [validators.Length(
        min=5, max=50,
        message="Email must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Username"})

    password = PasswordField('Password', [validators.Length(
        min=8, max=50,
        message="Password must be between 8 and 50 characters.")],
        render_kw={"placeholder": "Your Password"})

    submit = SubmitField('Login')


# Create a Form Class for Register Page
class RegisterForm(FlaskForm):

    username = StringField('Username', [validators.Length(
        min=5, max=50,
        message="Username must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Username"})

    email = EmailField('Email', [validators.Length(
        min=5, max=50,
        message="Email must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Email"})

    password = PasswordField('Password', [validators.Length(
        min=8, max=50,
        message="Password must be between 8 and 50 characters."),
        validators.EqualTo(
            "confirm_password", message='Passwords must match.')],
        render_kw={"placeholder": "Your Password"})

    confirm_password = PasswordField('Confirm Password', [validators.Length(
        min=8, max=50,
        message="Password must be between 8 and 50 characters.")],
        render_kw={"placeholder": "Confirm Password"})

    submit = SubmitField('Register')


# Create a Form Class for Edit Profile Page
class EditProfileForm(FlaskForm):

    first_name = StringField('First Name', [validators.Length(
        min=2, max=50,
        message="First Name must be between 2 and 50 characters.")],
        render_kw={"placeholder": "Your First Name"})

    last_name = StringField('Last Name', [validators.Length(
        min=2, max=50,
        message="Last Name must be between 2 and 50 characters.")],
        render_kw={"placeholder": "Your Last Name"})

    email = EmailField('Email', [validators.Length(
        min=5, max=50,
        message="Email must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Your Email"})

    submit = SubmitField('Update Profile')


# Creat a Form Class for adding an Article
class AddArticleForm(FlaskForm):

    title = StringField('Title', [validators.Length(
        min=5, max=50,
        message="Title must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Article Title"})
    
    preview = StringField('Preview', [validators.Length(
        min=5, max=50,
        message="Preview must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Article Preview"})

    content = CKEditorField('Content', [validators.Length(
        min=100,
        message="Content must be at least 100 characters.")],
        render_kw={"placeholder": "Article Content"})

    submit = SubmitField('Add Article')


# Create a Form Class for Edit Article Page
class Edit_Articles_Form(FlaskForm):

    title = StringField('Title', [validators.Length(
        min=5, max=50,
        message="Title must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Article Title"})
    
    preview = StringField('Preview', [validators.Length(
        min=5, max=50,
        message="Preview must be between 5 and 50 characters.")],
        render_kw={"placeholder": "Article Preview"})

    content = CKEditorField('Content', [validators.Length(
        min=100,
        message="Content must be at least 100 characters.")],
        render_kw={"placeholder": "Article Content"})

    submit = SubmitField('Update Article')