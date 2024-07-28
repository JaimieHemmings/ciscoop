import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from sqlalchemy.engine.url import make_url
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

database_url = os.environ.get('DATABASE_URL')
if database_url:
    parsed_url = make_url(database_url)
    if parsed_url.drivername == 'postgres':
        parsed_url.drivername = 'postgresql'
    SQLALCHEMY_DATABASE_URI = str(parsed_url)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from ciscoop import routes