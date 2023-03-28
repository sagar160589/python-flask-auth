from flask_login import login_manager, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing import db

db = SQLAlchemy()
login_manager = LoginManager()



##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB.
