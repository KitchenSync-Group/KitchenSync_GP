from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app import db

class PantryItem(db.Model):
    """Model for pantry items"""
    __tablename__ = 'pantry_items'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)
    
    def __init__(self, user_id, name, quantity, unit, category):
        self.user_id = user_id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.category = category
    
    def to_dict(self):
        """Convert the pantry item to a dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'category': self.category
        }
