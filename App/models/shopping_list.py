from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from app import db

class ShoppingListItem(db.Model):
    """Model for shopping list items"""
    __tablename__ = 'shopping_list_items'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String(20), nullable=True)
    purchased = Column(Boolean, default=False)
    
    def __init__(self, user_id, name, quantity, unit="", purchased=False):
        self.user_id = user_id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.purchased = purchased
    
    def to_dict(self):
        """Convert the shopping list item to a dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'purchased': self.purchased
        }
