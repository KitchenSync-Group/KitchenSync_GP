from app.models.pantry import PantryItem
from app import db

class PantryController:
    @staticmethod
    def get_user_pantry(user_id):
        """Get all pantry items for a user"""
        items = PantryItem.query.filter_by(user_id=user_id).all()
        return {str(item.id): item for item in items}
    
    @staticmethod
    def add_item(user_id, name, quantity, unit, category):
        """Add a new pantry item"""
        new_item = PantryItem(
            user_id=user_id,
            name=name,
            quantity=quantity,
            unit=unit,
            category=category
        )
        db.session.add(new_item)
        db.session.commit()
        return str(new_item.id)
    
    @staticmethod
    def update_item(item_id, quantity=None, unit=None, category=None):
        """Update a pantry item"""
        item = PantryItem.query.get(item_id)
        if not item:
            return False
        
        if quantity is not None:
            item.quantity = quantity
        if unit is not None:
            item.unit = unit
        if category is not None:
            item.category = category
        
        db.session.commit()
        return True
    
    @staticmethod
    def delete_item(item_id):
        """Delete a pantry item"""
        item = PantryItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_by_category(user_id, category):
        """Get pantry items by category"""
        items = PantryItem.query.filter_by(user_id=user_id, category=category).all()
        return {str(item.id): item for item in items}
    
    @staticmethod
    def get_ingredient_names(user_id):
        """Get just the ingredient names for recipe matching"""
        items = PantryItem.query.filter_by(user_id=user_id).all()
        return [item.name.lower() for item in items]

pantry_controller = PantryController()