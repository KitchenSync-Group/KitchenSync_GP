from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, JSON
from app import db

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    dietary_preferences = Column(JSON, nullable=True, default=list)
    
    def __init__(self, username, email, password_hash, dietary_preferences=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.dietary_preferences = dietary_preferences or []
    
    def get_id(self):
        return str(self.id)
    
    def to_dict(self):
        """Convert the user object to a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'dietary_preferences': self.dietary_preferences
        }