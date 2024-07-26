from ciscoop import db

class users(db.Model):
  # schema for users model
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(200), unique=False, nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  role = db.Column(db.String(20), unique=False, nullable=False, default="user")
  created = db.Column(db.DateTime, server_default=db.func.now())

  def __repr__(self):
      # return a string representation of the object
      return '<User %r>' % self.username
  
class posts(db.Model):
  # schema for posts model
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.Text, unique=False, nullable=False)
  created = db.Column(db.DateTime, server_default=db.func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  user = db.relationship('users', backref=db.backref('posts', lazy=True))

  def __repr__(self):
      # return a string representation of the object
      return '<Post %r>' % self.title
  
class messages(db.Model):
  # schema for messages model
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(120), unique=False, nullable=False)
  title = db.Column(db.String(80), unique=False, nullable=False)
  content = db.Column(db.String(280), unique=False, nullable=False)
  created = db.Column(db.DateTime, server_default=db.func.now())

  def __repr__(self):
      # return a string representation of the object
      return '<Message %r>' % self.title
