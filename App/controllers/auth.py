
from app.models.user import User
from app.database import db_session
from werkzeug.security import check_password_hash

def register_user(username, email, password, dietary_preferences=None):
    """Register a new user"""
    # Check if username or email already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return False, "Username or email already exists"
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    # Set dietary preferences if provided
    if dietary_preferences:
        if 'vegan' in dietary_preferences:
            user.is_vegan = True
        if 'vegetarian' in dietary_preferences:
            user.is_vegetarian = True
        if 'gluten_free' in dietary_preferences:
            user.is_gluten_free = True
        if 'dairy_free' in dietary_preferences:
            user.is_dairy_free = True
    
    # Save user to database
    db_session.add(user)
    db_session.commit()
    
    return True, "User registered successfully"

def authenticate_user(username, password):
    """Authenticate a user by username and password"""
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return None
    
    return user

def update_dietary_preferences(user_id, preferences):
    """Update user's dietary preferences"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"
    
    # Reset all preferences
    user.is_vegan = False
    user.is_vegetarian = False
    user.is_gluten_free = False
    user.is_dairy_free = False
    
    # Set selected preferences
    if 'vegan' in preferences:
        user.is_vegan = True
    if 'vegetarian' in preferences:
        user.is_vegetarian = True
    if 'gluten_free' in preferences:
        user.is_gluten_free = True
    if 'dairy_free' in preferences:
        user.is_dairy_free = True
    
    db_session.commit()
    
    return True, "Dietary preferences updated successfully"
