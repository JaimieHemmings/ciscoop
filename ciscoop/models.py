from ciscoop import db


class User(db.Model):
    # schema for User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(
        db.String(20), unique=False, nullable=False, default="user")
    created = db.Column(db.DateTime, server_default=db.func.now())
    first_name = db.Column(db.String(20), unique=False, nullable=True)
    last_name = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        # return a string representation of the object
        return '<User %r>' % self.username


class Post(db.Model):
    # schema for Post model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    preview = db.Column(db.String(50), unique=False, nullable=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Post', lazy=True))
    slug = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        # return a string representation of the object
        return '<Post %r>' % self.title


class Message(db.Model):
    # schema for Message model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(280), unique=False, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        # return a string representation of the object
        return '<Message %r>' % self.title


class Comment(db.Model):
    # schema for Comment model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.relationship(
        'User', backref=db.backref('Comment', lazy=True))
    content = db.Column(db.String(280), unique=False, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('Comment', lazy=True))

    def __repr__(self):
        # return a string representation of the object
        return '<Comment %r>' % self.name
