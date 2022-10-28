from flask_login import UserMixin, current_user
from flask import g

from app import db, manager, app
from datetime import datetime

# DB model News
class News(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    img = db.Column(db.String(200), nullable=True)
    description = db.Column(db.TEXT, nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
# DB model User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    token = db.Column(db.String(200), nullable=True)
    requests = db.Column(db.Integer(), nullable=True)
    escrow = db.Column(db.Integer(), nullable=True)
    balance = db.Column(db.Integer(), nullable=True)
    received = db.Column(db.Integer(), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    
    
class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@manager.user_loader
def load_user_admin(user_id):
    return UserAdmin.query.get(user_id)








