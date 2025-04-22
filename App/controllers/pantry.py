from app.models.pantry import PantryItem
from app.database import db_session
import datetime

def get_user_pantry(user_id):
    """Get all pantry items for a user"""
    return PantryItem.query.filter_by(user_id=user_id).all()

def get_pantry_item(item_id, user_id=None):
    """Get a specific pantry item"""
    query = PantryItem.query.filter_by(id=item_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.first()

def add_pantry_item(user_id, name, category, quantity=1, unit="", expiry_date=None):
    """Add a new item to the pantry"""
    # Check if item already exists for this user
    existing_item = PantryItem.query.filter_by(user_id=user_id, name=name).first()
    
    if existing_item:
        # Update quantity instead of creating new
        existing_item.quantity += quantity
        existing_item.updated_at = datetime.datetime.utcnow()
        db_session.commit()
        return existing_item
    
    # Create new item
    item = PantryItem(
        user_id=user_id,
        name=name,
        category=category,
        quantity=quantity,
        unit=unit,
        expiry_date=expiry_date
    )
    
    db_session.add(item)
    db_session.commit()
    
    return item

def update_pantry_item(item_id, user_id, **kwargs):
    """Update a pantry item"""
    item = get_pantry_item(item_id, user_id)
    if not item:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(item, key):
            setattr(item, key, value)
    
    item.updated_at = datetime.datetime.utcnow()
    db_session.commit()
    
    return item

def delete_pantry_item(item_id, user_id):
    """Delete a pantry item"""
    item = get_pantry_item(item_id, user_id)
    if not item:
        return False
    
    db_session.delete(item)
    db_session.commit()
    
    return True

def get_pantry_by_category(user_id):
    """Get pantry items grouped by category"""
    items = get_user_pantry(user_id)
    categorized = {}
    
    for item in items:
        if item.category not in categorized:
            categorized[item.category] = []
        categorized[item.category].append(item)
    
    return categorized