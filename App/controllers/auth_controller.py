from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

class AuthController:
    @staticmethod
    def register(username, password, email):
        """Register a new user"""
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return False, "Username already exists"
            
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return False, "Email already exists"
        
        # Create a new user
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        return True, new_user.id
    
    @staticmethod
    def login(username, password):
        """Login a user"""
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            return True, user
        
        return False, None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def update_dietary_preferences(user_id, preferences):
        """Update user's dietary preferences"""
        user = User.query.get(user_id)
        if user:
            user.dietary_preferences = preferences
            db.session.commit()
            return True
        return False

auth_controller = AuthController()